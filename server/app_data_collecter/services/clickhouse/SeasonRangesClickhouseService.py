
from typing import List, Optional
from project_box_score_arc.clickhouse_client import get_clickhouse_client

from ...models.clickhouse.SeasonRangeForClickhouseModel import SeasonRangeForClickhouse

class SeasonRangesClickhouseService:
    def __init__(self, table_name: str = "season_ranges"):
        self.client = get_clickhouse_client()
        self.table_name = table_name
        self._ensure_table_exists()


    def upsert_season_ranges(self, season_ranges: List[SeasonRangeForClickhouse]):
        if not season_ranges:
            return
            
        data = [
            (
                season_range.season,
                season_range.start_date,
                season_range.end_date,
                season_range.update_game_summaries_date
            )
            for season_range in season_ranges
        ]
        self.client.insert(self.table_name, data)
        self.client.command(f"OPTIMIZE TABLE {self.table_name} FINAL")

    def get_season_range(self, season: str) -> Optional[SeasonRangeForClickhouse]:
        query = f"SELECT * FROM {self.table_name} WHERE season = '{season}'"

        season_range_from_clickhouse = self.client.query(query).result_rows

        if len(season_range_from_clickhouse) == 0:
            return None
        else:
            return SeasonRangeForClickhouse(
                season=season_range_from_clickhouse[0][0],
                start_date=season_range_from_clickhouse[0][1],
                end_date=season_range_from_clickhouse[0][2],
                update_game_summaries_date=season_range_from_clickhouse[0][3]
            )

    def _ensure_table_exists(self):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            season String,
            start_date Date,
            end_date Date,
            update_game_summaries_date Date
        ) ENGINE = ReplacingMergeTree()
        PRIMARY KEY season
        """
        self.client.command(create_table_sql)