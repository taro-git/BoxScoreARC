from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .GameSummaryModel import TeamAbbreviation, TEAM_LOGO

@dataclass
class Player:
    player_id: int
    name: str
    position: str
    is_inactive: bool
    sequence: int

@dataclass(kw_only=True)
class TeamSummary:
    team_id: int
    abbreviation: TeamAbbreviation = 'Unknown'
    logo: str = field(init=False)
    players: List[Player]

    def __post_init__(self):
        self.logo = TEAM_LOGO.get(self.abbreviation, '')


@dataclass(kw_only=True)
class BoxScoreSummary:
    game_date_jst: datetime.date
    home: TeamSummary
    away: TeamSummary
