

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SeasonRangeForClickhouse:
    season: str
    start_date: datetime.date
    end_date: datetime.date
    update_game_summaries_date: datetime.date

