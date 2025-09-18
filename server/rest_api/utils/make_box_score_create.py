import copy
from typing import List

from rest_api.serializers.box_score import BoxScoreCreate, PlayerOnBoxScoreCreate


class BoxScoreCreateMaker:
    def __init__(
        self,
        game_id: str,
        final_seconds: int,
        home_players: List[PlayerOnBoxScoreCreate],
        away_players: List[PlayerOnBoxScoreCreate],
    ):
        self.game_id: str = game_id
        self.final_seconds: int = final_seconds
        self.home_players: List[PlayerOnBoxScoreCreate] = home_players
        self.away_players: List[PlayerOnBoxScoreCreate] = away_players

    def home_player_ids(self) -> List[int]:
        """ホームプレイヤーの player_id 一覧を返します"""
        return [player["player_id"] for player in self.home_players]

    def init_player(
        self,
        elapsed_seconds: int,
        player_id: int,
        is_home_player: bool,
        is_on_court: bool = True,
    ) -> None:
        """プレイヤーをボックススコアに追加します."""
        if player_id not in [player["player_id"] for player in self.home_players + self.away_players]:
            init_player_data = PlayerOnBoxScoreCreate(
                {
                    "player_id": player_id,
                    "box_score_data": [
                        {
                            "elapsed_seconds": elapsed_seconds,
                            "is_on_court": is_on_court,
                            "sec": 0,
                            "pts": 0,
                            "reb": 0,
                            "ast": 0,
                            "stl": 0,
                            "blk": 0,
                            "fg": 0,
                            "fga": 0,
                            "three": 0,
                            "threea": 0,
                            "ft": 0,
                            "fta": 0,
                            "oreb": 0,
                            "dreb": 0,
                            "to": 0,
                            "pf": 0,
                            "plusminus": 0,
                        }
                    ],
                }
            )
            if is_home_player:
                self.home_players.append(init_player_data)
            else:
                self.away_players.append(init_player_data)

    def append_box_score_data(
        self,
        elapsed_seconds: int,
        player_id: int,
        is_home_player: bool,
        keys: list[str],
        add_values: List[int],
    ) -> None:
        """ボックススコアにデータを追加します.
        keys と add_values のインデックスはそろえてください."""
        self.init_player(elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player["player_id"] == player_id:
                new_data = copy.deepcopy(player["box_score_data"][-1])
                new_data["elapsed_seconds"] = elapsed_seconds
                for i, key in enumerate(keys):
                    new_data[key] += add_values[i]
                player["box_score_data"].append(new_data)

    def players_to_bench(
        self,
        last_elapsed_seconds: int,
        elapsed_seconds: int,
        player_ids: List[int],
        is_home_player: bool,
    ) -> None:
        """player_ids で指定した選手一覧をベンチに移動させます.
        プレイヤーの初期追加が未実施の場合は実施します."""
        for player_id in player_ids:
            self.init_player(last_elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player["player_id"] in player_ids:
                data = player["box_score_data"]
                data.append(data[-1])
                data[-1]["elapsed_seconds"] = elapsed_seconds
                data[-1]["is_on_court"] = False

    def players_to_court(
        self,
        last_elapsed_seconds: int,
        elapsed_seconds: int,
        player_ids: List[int],
        is_home_player: bool,
    ) -> None:
        """player_ids で指定した選手一覧をコートに移動させます.
        プレイヤーの初期追加が未実施の場合は実施します."""
        for player_id in player_ids:
            self.init_player(last_elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player["player_id"] in player_ids:
                data = player["box_score_data"]
                data = player["box_score_data"]
                data.append(data[-1])
                data[-1]["elapsed_seconds"] = last_elapsed_seconds
                data[-1]["is_on_court"] = True
                data.append(data[-1])
                data[-1]["elapsed_seconds"] = elapsed_seconds
                data[-1]["is_on_court"] = True

    def to_box_score_create(self) -> BoxScoreCreate:
        """BoxScoreCreate クラスを生成します."""
        return BoxScoreCreate(
            {
                "game_id": self.game_id,
                "final_seconds": self.final_seconds,
                "home_players": self.home_players,
                "away_players": self.away_players,
            }
        )
