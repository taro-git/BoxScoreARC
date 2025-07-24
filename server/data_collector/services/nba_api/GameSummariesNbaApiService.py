from typing import List
from datetime import datetime, timedelta

from nba_api.stats.endpoints import leaguegamefinder, scoreboardv2

from ...models.nba_api.GameSummaryModel import GameSummary
from ..common.TimeAdjustService import TimeAdjustService


class GameSummariesNbaApiService:

    def __init__(self, timeAdjustService=None):
        self.timeAdjustService = timeAdjustService or TimeAdjustService()

    def get_recent_game_summaries(self, date_jst: datetime) -> List[GameSummary]:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=self.timeAdjustService.convert_tz_to_est(date_jst).strftime("%Y-%m-%d"))
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
                    game_date_jst=date_jst.date()
                )
            )
        
        return game_summaries
    
    def get_past_game_summaries(self, season: str) -> List[GameSummary]:
        league_game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season, league_id_nullable="00")
        league_game_finder_results = league_game_finder.league_game_finder_results.get_data_frame()

        game_summaries: List[GameSummary] = []
        game_ids = league_game_finder_results["GAME_ID"].drop_duplicates().tolist()

        for game_id in game_ids:
            teams_for_game = league_game_finder_results[league_game_finder_results["GAME_ID"] == game_id]
            game_date_jst = datetime.strptime(teams_for_game["GAME_DATE"].iloc[0], "%Y-%m-%d").date() + timedelta(days=1)
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
                    game_summaries.append(GameSummary(game_id=game_id, game_date_jst=game_date_jst))
                    continue
            else:
                game_summaries.append(GameSummary(game_id=game_id, game_date_jst=game_date_jst))
                continue
            game_summaries.append(
                GameSummary(
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
