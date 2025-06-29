from datetime import date
from typing import Literal
from dataclasses import dataclass, field

from ..postgres.GameSummaryForPostgresModel import GameSummaryForPostgres

TeamAbbreviation = Literal[
    'BOS', 'BKN', 'NYK', 'PHI', 'TOR', 'CHI', 'CLE', 'DET', 'IND', 'MIL', 'ATL', 'CHA', 'MIA', 'ORL', 'WAS',
    'DEN', 'MIN', 'OKC', 'POR', 'UTA', 'GSW', 'LAC', 'LAL', 'PHX', 'SAC', 'DAL', 'HOU', 'MEM', 'NOP', 'SAS',
    'Unknown'
]

TEAM_LOGO = {
    'BOS': 'https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg',
    'BKN': 'https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg',
    'NYK': 'https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg',
    'PHI': 'https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg',
    'TOR': 'https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg',
    'CHI': 'https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg',
    'CLE': 'https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg',
    'DET': 'https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg',
    'IND': 'https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg',
    'MIL': 'https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg',
    'ATL': 'https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg',
    'CHA': 'https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg',
    'MIA': 'https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg',
    'ORL': 'https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg',
    'WAS': 'https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg',
    'DEN': 'https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg',
    'MIN': 'https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg',
    'OKC': 'https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg',
    'POR': 'https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg',
    'UTA': 'https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg',
    'GSW': 'https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg',
    'LAC': 'https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg',
    'LAL': 'https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg',
    'PHX': 'https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg',
    'SAC': 'https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg',
    'DAL': 'https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg',
    'HOU': 'https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg',
    'MEM': 'https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg',
    'NOP': 'https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg',
    'SAS': 'https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg'
}

GAME_CATEGORY = {
    '1': 'Preseason',
    '2': 'Regular Season',
    '3': 'All Star',
    '4': 'Playoffs',
    '5': 'Play-In Tournament',
    '6': 'Emirates NBA Cup'
}

@dataclass(kw_only=True)
class GameSummary:
    game_id: str
    home_team: TeamAbbreviation = 'Unknown'
    home_logo: str = field(init=False)
    home_score: int = 0
    away_team: TeamAbbreviation = 'Unknown'
    away_logo: str = field(init=False)
    away_score: int = 0
    game_sequence: int = 0
    status_id: int = 3 # 1: scheduled, 2: game started, 3: game finished
    status_text: str = 'Final' # status_id=1 -> h:mm pm/am ET, status_id=2 -> 1st Qtr etc., status_id=3 -> Final
    live_period: int = 4
    live_clock: str = '00:00'
    game_date_jst: date
    game_category: str = field(init=False)

    def __post_init__(self):
        self.home_logo = TEAM_LOGO.get(self.home_team, '')
        self.away_logo = TEAM_LOGO.get(self.away_team,'')
        self.game_category = GAME_CATEGORY.get(self.game_id[2], 'Unknown')

    @classmethod
    def from_postgres_model(cls, model: GameSummaryForPostgres) -> "GameSummary":
        return cls(
            game_id=model.game_id,
            home_team=model.home_team,
            home_score=model.home_score,
            away_team=model.away_team,
            away_score=model.away_score,
            game_sequence=model.game_sequence,
            status_id=model.status_id,
            status_text=model.status_text,
            live_period=model.live_period,
            live_clock=model.live_clock,
            game_date_jst=model.game_date_jst
        )

    def to_postgres_model(self) -> GameSummaryForPostgres:
        return GameSummaryForPostgres(
            game_id=self.game_id,
            home_team=self.home_team,
            home_score=self.home_score,
            away_team=self.away_team,
            away_score=self.away_score,
            game_sequence=self.game_sequence,
            status_id=self.status_id,
            status_text=self.status_text,
            live_period=self.live_period,
            live_clock=self.live_clock,
            game_date_jst=self.game_date_jst
        )
