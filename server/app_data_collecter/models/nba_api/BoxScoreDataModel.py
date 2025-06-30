from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from ..postgres.BoxScoreDataForPostgresModel import BoxScoreDataForPostgres

@dataclass
class BoxScoreData:
    game_id: str
    data: Dict[int, List[Tuple[int, List[int]]]] = field(default_factory=lambda: defaultdict(list))

    @classmethod
    def from_postgres_model(cls, model: BoxScoreDataForPostgres) -> "BoxScoreData":
        converted_data = defaultdict(list)
        for k, v in model.data.items():
            converted_data[int(k)] = [(int(player_id), stats) for player_id, stats in v]
        return cls(
            game_id=model.game_id,
            data=converted_data
        )

    def to_postgres_model(self) -> BoxScoreDataForPostgres:
        json_data = {
            str(k): [[player_id, stats] for player_id, stats in v]
            for k, v in self.data.items()
        }
        return BoxScoreDataForPostgres(
            game_id=self.game_id,
            data=json_data
        )
