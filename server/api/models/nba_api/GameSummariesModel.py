from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

from nba_api.stats.endpoints import boxscoresummaryv2
from ...services.common.TimeDiffAdjustService import combine_date_and_time


@dataclass
class GameSummary:
    game_id: str
    home_team: str
    away_team: str
    start_time_est: datetime
    status_id: int
    live_period: Optional[int]
    live_clock: Optional[str]


def get_game_summaries(game_ids: List[str]) -> List[GameSummary]:
    summaries = []

    for game_id in game_ids:
        boxscore = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        game_summary_df = boxscore.game_summary.get_data_frame()
        line_score_df = boxscore.line_score.get_data_frame()

        if game_summary_df.empty or line_score_df.empty:
            continue

        game_date = game_summary_df.loc[0, 'GAME_DATE_EST']
        status_id = game_summary_df.loc[0, 'GAME_STATUS_ID']
        if status_id == 1:
            game_time = game_summary_df.loc[0, 'GAME_STATUS_TEXT']
            start_time_est = combine_date_and_time(game_date, game_time)
        else:
            start_time_est = combine_date_and_time(game_date, '8:00 pm ET')

        period = game_summary_df.loc[0].get('LIVE_PERIOD')
        clock = game_summary_df.loc[0].get('LIVE_PC_TIME')

        home_team = ''
        away_team = ''
        for _, row in line_score_df.iterrows():
            if row['TEAM_ID'] == game_summary_df.loc[0, 'HOME_TEAM_ID']:
                home_team = row['TEAM_ABBREVIATION']
            else:
                away_team = row['TEAM_ABBREVIATION']

        summaries.append(GameSummary(
            game_id=game_id,
            home_team=home_team,
            away_team=away_team,
            start_time_est=start_time_est,
            status_id=status_id,
            live_period=period if not pd.isna(period) else None,
            live_clock=clock if isinstance(clock, str) else None
        ))

    return summaries
