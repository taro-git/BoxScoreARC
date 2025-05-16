from typing import List
from datetime import datetime

from nba_api.stats.endpoints import scoreboardv2

from ...models.nba_api.GameSummaryModel import GameSummary
from ..common.TimeAdjustService import TimeAdjustService


class GetGameSummariesService:

    def __init__(self, timeAdjustService=None):
        self.timeAdjustService = timeAdjustService or TimeAdjustService()

    def get_game_summaries_for_date(self, date: str) -> List[GameSummary]:
        date_est = self.timeAdjustService.convert_tz_to_est(
            self.timeAdjustService.convert_tz_to_jst(
                self.timeAdjustService.convert_date_str_to_datetime(date)
            )
        )
        game_summaries = self._get_game_summaries_from_nba_api(date_est)
        return self._sort_game_summaries(self._convert_status_text(game_summaries, date_est))

    def _get_game_summaries_from_nba_api(self, date: datetime) -> List[GameSummary]:
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

    def _sort_game_summaries(self, games: List[GameSummary]) -> List[GameSummary]:
        status_id_priority = {
            2: 0, # playing
            1: 1, # scheduled
            3: 2 # finished
        }
        return sorted(games, key = lambda game: (status_id_priority[game.status_id], game.game_sequence))

    def _convert_status_text(self, game_summaries: List[GameSummary], date_est: datetime) -> List[GameSummary]:
        for game_summary in filter(lambda gs: gs.status_id == 1, game_summaries):
            time = self.timeAdjustService.convert_time_str_to_datetime(game_summary.status_text)
            datetime_est = time.replace(year=date_est.year, month=date_est.month, day=date_est.day)
            game_summary.status_text = self.timeAdjustService.convert_tz_to_jst(datetime_est).strftime("%H:%M")
        return game_summaries
