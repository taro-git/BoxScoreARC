from dataclasses import dataclass
from datetime import datetime

from ..nba_api.GameSummaryModel import GameSummary, TEAM_LOGO, GAME_CATEGORY

@dataclass(kw_only=True)
class GameSummaryForClickhouse(GameSummary):
    game_date_jst: datetime.date
