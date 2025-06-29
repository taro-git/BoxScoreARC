import pandas as pd
from typing import List
from datetime import datetime, timedelta

from ...models.nba_api.GameSummaryModel import GameSummary
from ...models.postgres.GameSummaryForPostgresModel import GameSummaryForPostgres
from ...models.postgres.SeasonRangeForPostgresModel import SeasonRangeForPostgres
from .TimeAdjustService import TimeAdjustService
from ..nba_api.GameSummariesNbaApiService import GameSummariesNbaApiService


class GetGameSummariesService:

    def __init__(self, timeAdjustService=None, gameSummariesNbaApiService=None, gameSummariesClickhouseService=None, seasonRangeClickhouseService=None):
        self.timeAdjustService = timeAdjustService or TimeAdjustService()
        self.gameSummariesNbaApiService = gameSummariesNbaApiService or GameSummariesNbaApiService()

    def get_game_summaries_for_date(self, date_jst: datetime) -> List[GameSummary]:
        date_est = self.timeAdjustService.convert_tz_to_est(date_jst)
        today_jst = self.timeAdjustService.today_jst()

        game_summaries = []
        if date_jst.date() < today_jst - timedelta(days=1):
            season_strings = self._get_season_strings(date_jst)

            prev_season_str = season_strings["prev_season"]
            prev_season_range = SeasonRangeForPostgres.objects.filter(season=prev_season_str).first()
            if prev_season_range == None:
                self._update_postgres_game_summaries_and_season_range(prev_season_str, today_jst)
                prev_season_range = SeasonRangeForPostgres.objects.filter(season=prev_season_str).first()

            next_season_str = season_strings["next_season"]
            next_season_range = SeasonRangeForPostgres.objects.filter(season=next_season_str).first()
            if prev_season_range.end_date < date_jst.date():
                if next_season_range == None:
                    self._update_postgres_game_summaries_and_season_range(prev_season_str, today_jst)
                    next_season_range = SeasonRangeForPostgres.objects.filter(season=next_season_str).first()
                if next_season_range == None and prev_season_range.update_game_summaries_date < date_jst.date():
                    self._update_postgres_game_summaries_and_season_range(prev_season_str, today_jst)
            
            game_summary_postgres_models = GameSummaryForPostgres.objects.filter(game_date_jst=date_jst)
            game_summaries = [GameSummary.from_postgres_model(game_summary_postgres_model) for game_summary_postgres_model in game_summary_postgres_models]
        else:
            game_summaries = self.gameSummariesNbaApiService.get_recent_game_summaries(date_jst)
        return self._sort_game_summaries(self._convert_status_text(game_summaries, date_est))
    
    def _update_postgres_game_summaries_and_season_range(self, season: str, today_jst: datetime.date):
        game_summaries_from_nba_api_for_past: List[GameSummary] = self.gameSummariesNbaApiService.get_past_game_summaries(season)
        if len(game_summaries_from_nba_api_for_past) != 0:
            season_range_postgres_model : SeasonRangeForPostgres = SeasonRangeForPostgres(
                season=season,
                start_date=min(
                    game_summaries_from_nba_api_for_past,
                    key=lambda game_summary: game_summary.game_date_jst
                ).game_date_jst,
                end_date=max(
                    game_summaries_from_nba_api_for_past,
                    key=lambda game_summary: game_summary.game_date_jst
                ).game_date_jst,
                update_game_summaries_date=today_jst
            )
            season_range_postgres_model.upsert()
        for game_summary in game_summaries_from_nba_api_for_past:
            game_summary_postgres_model: GameSummaryForPostgres = game_summary.to_postgres_model()
            game_summary_postgres_model.upsert()
            
    
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
