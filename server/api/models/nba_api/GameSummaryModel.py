from typing import Literal
from dataclasses import dataclass

TeamAbbreviation = Literal[
    'ORL', 'ATL', 'CHA', 'BOS', 'NYK', 'BKN', 'IND', 'CLE', 'WAS', 'MIA', 'CHI', 'PHI', 'DET', 'MIL', 'TOR',
    'DEN', 'HOU', 'DAL', 'MEM', 'UTA', 'MIN', 'OKC', 'NOP', 'SAS', 'LAC', 'GSW', 'LAL', 'POR', 'PHX', 'SAC'
]

@dataclass
class GameSummary:
    game_id: str
    home_team: TeamAbbreviation
    home_score: int
    away_team: TeamAbbreviation
    away_score: int
    game_sequence: int
    status_id: int # 1: scheduled, 2: game started, 3: game finished
    status_text: str # status_id=1 -> h:mm pm/am ET, status_id=2 -> 1st Qtr etc., status_id=3 -> Final
    live_period: int
    live_clock: str

