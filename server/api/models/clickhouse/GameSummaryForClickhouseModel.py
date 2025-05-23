from dataclasses import dataclass
from datetime import datetime

from ..nba_api.GameSummaryModel import GameSummary, TEAM_LOGO

@dataclass(kw_only=True)
class GameSummaryForClickhouse(GameSummary):
    game_date_jst: datetime.date
