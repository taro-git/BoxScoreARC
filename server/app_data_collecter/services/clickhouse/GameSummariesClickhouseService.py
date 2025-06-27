from dataclasses import asdict
from datetime import datetime, timedelta
from typing import List

from project_box_score_arc.clickhouse_client import get_clickhouse_client
from ...models.nba_api.GameSummaryModel import GameSummary
from ...models.clickhouse.GameSummaryForClickhouseModel import GameSummaryForClickhouse


class GameSummariesClickhouseService:
    def __init__(self, table_name: str = "game_summaries"):
        self.client = get_clickhouse_client()
        self.table_name = table_name
        self._ensure_table_exists()

    def upsert_game_summaries(self, game_summaries: List[GameSummaryForClickhouse]):
        if not game_summaries:
            return

        game_ids = [game_summary.game_id for game_summary in game_summaries]
        existing_ids = self._get_existing_game_ids(game_ids)

        filtered_game_summaries = [game_summary for game_summary in game_summaries if game_summary.game_id not in existing_ids]
        if not filtered_game_summaries:
            return

        data = [
            (
                game_summary.game_id,
                game_summary.home_team,
                game_summary.home_score,
                game_summary.away_team,
                game_summary.away_score,
                game_summary.game_sequence,
                game_summary.live_period,
                game_summary.game_date_jst
            )
            for game_summary in filtered_game_summaries
        ]
        self.client.insert(self.table_name, data)
        self.client.command(f"OPTIMIZE TABLE {self.table_name} FINAL")

    def get_game_summaries_for_date(self, date_jst: datetime) -> List[GameSummary]:
        game_summaries_from_clickhouse = self.get_game_summaries(game_date_jst=date_jst.strftime("%Y-%m-%d"))
        return [
            GameSummary(
                game_id=game_summary_for_clickhouse.game_id,
                home_team=game_summary_for_clickhouse.home_team,
                home_score=game_summary_for_clickhouse.home_score,
                away_team=game_summary_for_clickhouse.away_team,
                away_score=game_summary_for_clickhouse.away_score,
                game_sequence=game_summary_for_clickhouse.game_sequence,
                status_id=game_summary_for_clickhouse.status_id,
                status_text=game_summary_for_clickhouse.status_text,
                live_period=game_summary_for_clickhouse.live_period,
                live_clock=game_summary_for_clickhouse.live_clock,
            )
            for game_summary_for_clickhouse in game_summaries_from_clickhouse
        ]

    def get_game_summaries(
        self,
        game_id: str = None,
        game_date_jst: str = None,
        home_team: str = None,
        away_team: str = None
    ) -> List[GameSummaryForClickhouse]:
        conditions = []
        if game_id:
            conditions.append(f"game_id = '{game_id}'")
        if game_date_jst:
            conditions.append(f"game_date_jst = '{game_date_jst}'")
        if home_team:
            conditions.append(f"home_team = '{home_team}'")
        if away_team:
            conditions.append(f"away_team = '{away_team}'")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"SELECT * FROM {self.table_name} {where_clause}"

        game_summaries_from_clickhouse = self.client.query(query)

        return [
            GameSummaryForClickhouse(
                game_id=game_summary_from_clickhouse[0],
                home_team=game_summary_from_clickhouse[1],
                home_score=game_summary_from_clickhouse[2],
                away_team=game_summary_from_clickhouse[3],
                away_score=game_summary_from_clickhouse[4],
                game_sequence=game_summary_from_clickhouse[5],
                status_id=3,
                status_text='Final',
                live_period=game_summary_from_clickhouse[6],
                live_clock='00:00',
                game_date_jst=game_summary_from_clickhouse[7],
            )
            for game_summary_from_clickhouse in game_summaries_from_clickhouse.result_rows
        ]

    def _ensure_table_exists(self):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            game_id String,
            home_team String,
            home_score Int32,
            away_team String,
            away_score Int32,
            game_sequence Int32,
            live_period Int32,
            game_date_jst Date
        ) ENGINE = ReplacingMergeTree()
        PRIMARY KEY game_id
        """
        self.client.command(create_table_sql)

    def _get_existing_game_ids(self, game_ids: List[str]) -> set:
        joined_ids = "', '".join(game_ids)
        query = f"""
        SELECT game_id FROM {self.table_name}
        WHERE game_id IN ('{joined_ids}')
        """
        result = self.client.query(query)
        return {row[0] for row in result.result_rows}
