import pandas as pd
from typing import List
from datetime import datetime, timedelta

from nba_api.stats.endpoints import leaguegamefinder, scoreboardv2

from ...models.clickhouse.GameSummaryForClickhouseModel import GameSummaryForClickhouse
from ...models.clickhouse.SeasonRangeForClickhouseModel import SeasonRangeForClickhouse
from ...models.nba_api.GameSummaryModel import GameSummary
from ..common.TimeAdjustService import TimeAdjustService
from ..clickhouse.GameSummariesClickhouseService import GameSummariesClickhouseService
from ..clickhouse.SeasonRangesClickhouseService import SeasonRangesClickhouseService


class GetGameSummariesService:

    def __init__(self, timeAdjustService=None, gameSummariesClickhouseService=None, seasonRangeClickhouseService=None):
        self.timeAdjustService = timeAdjustService or TimeAdjustService()
        self.gameSummariesClickhouseService = gameSummariesClickhouseService or GameSummariesClickhouseService()
        self.seasonRangeClickhouseService = seasonRangeClickhouseService or SeasonRangesClickhouseService()

    def get_game_summaries_for_date(self, date: str) -> List[GameSummary]:
        date_jst = self.timeAdjustService.convert_tz_to_jst(
            self.timeAdjustService.convert_date_str_to_datetime(date)
        )
        date_est = self.timeAdjustService.convert_tz_to_est(date_jst)
        today_jst = self.timeAdjustService.today_jst()
        

        game_summaries = []
        if date_jst.date() < today_jst - timedelta(days=1):
            season_strings = self._get_season_strings(date_jst)

            prev_season_str = season_strings["prev_season"]
            prev_season_range = self.seasonRangeClickhouseService.get_season_range(prev_season_str)
            if prev_season_range == None:
                self._update_clickhouse_game_summaries_and_season_range(prev_season_str, today_jst)
                prev_season_range = self.seasonRangeClickhouseService.get_season_range(prev_season_str)

            next_season_str = season_strings["next_season"]
            next_season_range = self.seasonRangeClickhouseService.get_season_range(next_season_str)
            if prev_season_range.end_date < date_jst.date():
                if next_season_range == None:
                    self._update_clickhouse_game_summaries_and_season_range(next_season_str, today_jst)
                    next_season_range = self.seasonRangeClickhouseService.get_season_range(next_season_str)
                if next_season_range == None and prev_season_range.update_game_summaries_date < date_jst.date():
                    self._update_clickhouse_game_summaries_and_season_range(prev_season_str, today_jst)
            
            game_summaries = self.gameSummariesClickhouseService.get_game_summaries_for_date(date_jst)
        else:
            game_summaries = self._get_game_summaries_from_nba_api_for_recent(date_est)
        return self._sort_game_summaries(self._convert_status_text(game_summaries, date_est))
    
    def _update_clickhouse_game_summaries_and_season_range(self, season: str, today_jst: datetime.date):
        game_summaries_from_nba_api_for_past = self._get_game_summaries_from_nba_api_for_past(season)
        if len(game_summaries_from_nba_api_for_past) != 0:
            self.seasonRangeClickhouseService.upsert_season_ranges([SeasonRangeForClickhouse(
                season=season,
                start_date=min(
                    game_summaries_from_nba_api_for_past,
                    key=lambda game_summary_for_clickhouuse: game_summary_for_clickhouuse.game_date_jst
                ).game_date_jst,
                end_date=max(
                    game_summaries_from_nba_api_for_past,
                    key=lambda game_summary_for_clickhouuse: game_summary_for_clickhouuse.game_date_jst
                ).game_date_jst,
                update_game_summaries_date=today_jst
            )])
        self.gameSummariesClickhouseService.upsert_game_summaries(game_summaries_from_nba_api_for_past)

    def _get_game_summaries_from_nba_api_for_recent(self, date: datetime) -> List[GameSummary]:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date.strftime("%Y-%m-%d"))
        game_header = scoreboard.game_header.get_data_frame()
        line_score = scoreboard.line_score.get_data_frame()

        game_summaries: List[GameSummary] = []
        game_ids = game_header["GAME_ID"].tolist()
        
        for game_id in game_ids:
            filtered_game_header = game_header[game_header["GAME_ID"] == game_id][["GAME_STATUS_ID", "GAME_STATUS_TEXT", "LIVE_PERIOD", "LIVE_PC_TIME", "HOME_TEAM_ID"]]
            filtered_line_score = line_score[line_score["GAME_ID"] == game_id][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS", "TEAM_ID"]]
            home_team_line_score = filtered_line_score[filtered_line_score["TEAM_ID"] == filtered_game_header["HOME_TEAM_ID"].iloc[0]][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS"]]
            away_team_line_score = filtered_line_score[filtered_line_score["TEAM_ID"] != filtered_game_header["HOME_TEAM_ID"].iloc[0]][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS"]]
            game_summaries.append(
                GameSummary(
                    game_id=game_id,
                    home_team=home_team_line_score["TEAM_ABBREVIATION"].iloc[0],
                    home_score=home_team_line_score["PTS"].iloc[0],
                    away_team=away_team_line_score["TEAM_ABBREVIATION"].iloc[0],
                    away_score=away_team_line_score["PTS"].iloc[0],
                    game_sequence=home_team_line_score["GAME_SEQUENCE"].iloc[0],
                    status_id=filtered_game_header["GAME_STATUS_ID"].iloc[0],
                    status_text=filtered_game_header["GAME_STATUS_TEXT"].iloc[0],
                    live_period=filtered_game_header["LIVE_PERIOD"].iloc[0],
                    live_clock=filtered_game_header["LIVE_PC_TIME"].iloc[0],
                )
            )
        
        return game_summaries
    
    def _get_season_strings(self, datetime: datetime) -> dict[str, str]:
        year = datetime.year
        prev_year = year - 1
        next_year = year + 1
        return {
            "prev_season": f"{prev_year}-{str(year)[-2:]}",
            "next_season": f"{year}-{str(next_year)[-2:]}"
        }
    
    def _get_game_summaries_from_nba_api_for_past(self, season: str) -> List[GameSummaryForClickhouse]:
        league_game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season)
        league_game_finder_results = league_game_finder.league_game_finder_results.get_data_frame()

        game_summaries: List[GameSummaryForClickhouse] = []
        game_ids = league_game_finder_results["GAME_ID"].drop_duplicates().tolist()

        for game_id in game_ids:
            teams_for_game = league_game_finder_results[league_game_finder_results["GAME_ID"] == game_id]
            game_date_jst = datetime.strptime(teams_for_game["GAME_DATE"].iloc[0], "%Y-%m-%d").date() + timedelta(days=1)
            print(game_date_jst)
            if len(teams_for_game) == 2:
                matchup_str = teams_for_game["MATCHUP"].iloc[0]
                if 'vs.' in matchup_str:
                    home_team_abbreviation = matchup_str[:3]
                elif '@' in matchup_str:
                    home_team_abbreviation = matchup_str[-3:]
                else:
                    raise ValueError(f"String of MATCHUP {matchup_str} in GAME_ID {game_id} does not contain vs. or @.")
                home_team = teams_for_game[teams_for_game["TEAM_ABBREVIATION"] == home_team_abbreviation]
                away_team = teams_for_game[teams_for_game["TEAM_ABBREVIATION"] != home_team_abbreviation]
                if len(home_team) != 1 or len(away_team) != 1:
                    game_summaries.append(GameSummaryForClickhouse(game_id=game_id, game_date_jst=game_date_jst))
                    continue
            else:
                game_summaries.append(GameSummaryForClickhouse(game_id=game_id, game_date_jst=game_date_jst))
                continue
            game_summaries.append(
                GameSummaryForClickhouse(
                    game_id=game_id,
                    home_team=home_team["TEAM_ABBREVIATION"].iloc[0],
                    home_score=home_team["PTS"].iloc[0],
                    away_team=away_team["TEAM_ABBREVIATION"].iloc[0],
                    away_score=away_team["PTS"].iloc[0],
                    live_period=4 + (home_team["MIN"].iloc[0] - 240)//25,
                    game_date_jst=game_date_jst
                )
            )
        return game_summaries

    def _sort_game_summaries(self, games: List[GameSummary]) -> List[GameSummary]:
        status_id_priority = {
            2: 0, # playing
            1: 1, # scheduled
            3: 2 # finished
        }
        return sorted(games, key = lambda game: (status_id_priority[game.status_id], game.game_sequence, game.game_id))

    def _convert_status_text(self, game_summaries: List[GameSummary], date_est: datetime) -> List[GameSummary]:
        for game_summary in filter(lambda gs: gs.status_id == 1, game_summaries):
            time = self.timeAdjustService.convert_time_str_to_datetime(game_summary.status_text)
            datetime_est = time.replace(year=date_est.year, month=date_est.month, day=date_est.day)
            game_summary.status_text = self.timeAdjustService.convert_tz_to_jst(datetime_est).strftime("%H:%M")
        return game_summaries
