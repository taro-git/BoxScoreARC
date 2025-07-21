from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from .GameSummaryModel import TeamAbbreviation, TEAM_LOGO, fetch_and_encode_svg
from ..postgres.BoxScoreSummaryForPostgresModel import BoxScoreSummaryForPostgres

@dataclass
class Player:
    player_id: int
    name: str
    jersey: str
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
        self.logo = fetch_and_encode_svg(TEAM_LOGO.get(self.abbreviation, ''))


@dataclass(kw_only=True)
class BoxScoreSummary:
    game_id: str
    game_date_jst: datetime.date
    home: TeamSummary
    away: TeamSummary

    @classmethod
    def from_postgres_model(cls, model: BoxScoreSummaryForPostgres) -> "BoxScoreSummary":
        return cls(
            game_id=model.game_id,
            game_date_jst=model.game_date_jst,
            home=cls._dict_to_team(model.home),
            away=cls._dict_to_team(model.away),
        )

    def to_postgres_model(self) -> BoxScoreSummaryForPostgres:
        return BoxScoreSummaryForPostgres(
            game_id=self.game_id,
            game_date_jst=self.game_date_jst,
            home=self._team_to_dict(self.home),
            away=self._team_to_dict(self.away),
        )

    @staticmethod
    def _team_to_dict(team: TeamSummary) -> Dict[str, Any]:
        return {
            "team_id": team.team_id,
            "abbreviation": team.abbreviation,
            "players": [asdict(p) for p in team.players],
        }

    @staticmethod
    def _dict_to_team(data: Dict[str, Any]) -> TeamSummary:
        players = [Player(**p) for p in data.get("players", [])]
        return TeamSummary(
            team_id=data["team_id"],
            abbreviation=data.get("abbreviation", "Unknown"),
            players=players
        )