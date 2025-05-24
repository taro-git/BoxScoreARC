import pandas as pd
from typing import List
from datetime import datetime, timedelta

from ...models.clickhouse.GameSummaryForClickhouseModel import GameSummaryForClickhouse
from ...models.clickhouse.SeasonRangeForClickhouseModel import SeasonRangeForClickhouse
from ...models.nba_api.GameSummaryModel import GameSummary
from .TimeAdjustService import TimeAdjustService
from ..nba_api.GameSummariesNbaApiService import GameSummariesNbaApiService
from ..clickhouse.GameSummariesClickhouseService import GameSummariesClickhouseService
from ..clickhouse.SeasonRangesClickhouseService import SeasonRangesClickhouseService


class GetGameSummariesService:

    def __init__(self, timeAdjustService=None, gameSummariesNbaApiService=None, gameSummariesClickhouseService=None, seasonRangeClickhouseService=None):
        self.timeAdjustService = timeAdjustService or TimeAdjustService()
        self.gameSummariesClickhouseService = gameSummariesClickhouseService or GameSummariesClickhouseService()
        self.seasonRangeClickhouseService = seasonRangeClickhouseService or SeasonRangesClickhouseService()
        self.gameSummariesNbaApiService = gameSummariesNbaApiService or GameSummariesNbaApiService()

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
            game_summaries = self.gameSummariesNbaApiService.get_recent_game_summaries(date_est)
        return self._sort_game_summaries(self._convert_status_text(game_summaries, date_est))
    
    def _update_clickhouse_game_summaries_and_season_range(self, season: str, today_jst: datetime.date):
        game_summaries_from_nba_api_for_past: GameSummaryForClickhouse = self.gameSummariesNbaApiService.get_past_game_summaries_for_clickhouse(season)
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
    
    def _get_season_strings(self, datetime: datetime) -> dict[str, str]:
        year = datetime.year
        prev_year = year - 1
        next_year = year + 1
        return {
            "prev_season": f"{prev_year}-{str(year)[-2:]}",
            "next_season": f"{year}-{str(next_year)[-2:]}"
        }

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
