from typing import List
from datetime import datetime

from nba_api.stats.endpoints import scoreboardv2

from ...models.nba_api.GameSummaryModel import GameSummary
from ..common.TimeAdjustService import TimeAdjustService


class GetGameSummariesService:

    timeadjustService = TimeAdjustService()

    game_summaries: List[GameSummary] = []

    def get_game_summaries_for_date(self, date: str) -> List[GameSummary]:
        date_est = self.timeadjustService.convert_tz_to_est(
            self.timeadjustService.convert_tz_to_jst(
                self.timeadjustService.convert_type_str_to_date(date)
            )
        )
        self.game_summaries = []
        self._get_game_summaries_from_nba_api(date_est)
        return self.game_summaries

    def _get_game_summaries_from_nba_api(self, date: datetime):
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date.strftime("%Y-%m-%d"))
        game_header = scoreboard.game_header.get_data_frame()
        line_score = scoreboard.line_score.get_data_frame()
        game_ids = game_header["GAME_ID"].tolist()
        
        for game_id in game_ids:
            filtered_game_header = game_header[game_header["GAME_ID"] == game_id][["GAME_STATUS_ID", "GAME_STATUS_TEXT", "LIVE_PERIOD", "LIVE_PC_TIME", "HOME_TEAM_ID"]]
            filtered_line_score = line_score[line_score["GAME_ID"] == game_id][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS", "TEAM_ID"]]
            home_team_line_score = filtered_line_score[filtered_line_score["TEAM_ID"] == filtered_game_header["HOME_TEAM_ID"].iloc[0]][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS"]]
            away_team_line_score = filtered_line_score[filtered_line_score["TEAM_ID"] != filtered_game_header["HOME_TEAM_ID"].iloc[0]][["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS"]]
            self.game_summaries.append(
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

    #TODO implement sort
    def _sort_game_suummaries(self, games: List[GameSummary]) -> List[GameSummary]:

        def sort_key(game: GameSummary):
            status_id = game["status_id"]
            game_id = game["game_id"]
            start_time = datetime.fromisoformat(game["start_time"])

            if status == "PLAYING":
                # live_clock は "2:30" のような文字列だと仮定して変換（例: "2:30" → 150）
                def clock_to_seconds(clock_str):
                    try:
                        minutes, seconds = map(int, clock_str.split(":"))
                        return minutes * 60 + seconds
                    except:
                        return float("inf")  # パースできない場合は最大値

                return (
                    status_id,
                    -game["live_period"],
                    clock_to_seconds(game["live_clock"]),
                    game_id
                )
            else:
                return (
                    status_id,
                    start_time,
                    game_id
                )

        return sorted(games, key=sort_key)

    #TODO implement sort
    def _convert_status_text(self, status_text: str, date: datetime) -> str:
        temp = self.timeadjustService.convert_type_str_to_date(status_text)
        #temp の時間にdateの日付つける
        #日本時間にcoonvert
        #時間を抽出して文字列に
        converted_text = temp
        return converted_text
