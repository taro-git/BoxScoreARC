from datetime import datetime
from typing import Any, TypedDict, cast

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from rest_api.models.game_summary import GameSummary, PlayerOnGame, Team


##
## schema for access from django self
####
class PlayerOnGameCreate(TypedDict):
    player_id: int
    name: str
    jersey: str
    position: str
    is_starter: bool
    is_inactive: bool
    sequence: int


class GameSummaryCreate(TypedDict):
    game_id: int
    sequence: int
    status_id: int
    """1: scheduled, 2: game started, 3: game finished"""
    status_text: str
    """status_id=1 -> h:mm pm/am ET, status_id=2 -> 1st Qtr etc., status_id=3 -> Final"""
    game_datetime: datetime
    home_team_id: int
    away_team_id: int
    home_team_abb: str
    away_team_abb: str
    home_score: int
    away_score: int
    home_players: list[PlayerOnGameCreate]
    away_players: list[PlayerOnGameCreate]


##
## Serializer
####
class TeamSerializer(serializers.ModelSerializer[Team]):
    class Meta:  # type: ignore
        model = Team
        fields = "__all__"


class PlayerOnGameSerializer(serializers.ModelSerializer[PlayerOnGame]):
    class Meta:  # type: ignore
        model = PlayerOnGame
        fields = [
            "player_id",
            "name",
            "jersey",
            "position",
            "is_starter",
            "is_inactive",
            "sequence",
        ]


class GameSummarySerializer(serializers.ModelSerializer[GameSummary]):
    home_players = PlayerOnGameSerializer(many=True, source="home_players_on_game")
    away_players = PlayerOnGameSerializer(many=True, source="away_players_on_game")
    game_category = serializers.SerializerMethodField()
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    home_team_id = cast(
        PrimaryKeyRelatedField[Team],
        serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="home_team", write_only=True),
    )
    away_team_id = cast(
        PrimaryKeyRelatedField[Team],
        serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="away_team", write_only=True),
    )

    class Meta:  # type: ignore
        model = GameSummary
        fields = "__all__"

    def get_game_category(self, obj: GameSummary) -> str:
        return obj.game_category

    def create(self, validated_data: GameSummaryCreate):
        home_players_data = cast(list[PlayerOnGameCreate], validated_data.pop("home_players_on_game", []))
        away_players_data = cast(list[PlayerOnGameCreate], validated_data.pop("away_players_on_game", []))
        game = GameSummary.objects.create(**validated_data)
        for home_player_data in home_players_data:
            PlayerOnGame.objects.create(game_id=game, is_home=True, **home_player_data)
        for away_player_data in away_players_data:
            PlayerOnGame.objects.create(game_id=game, is_home=False, **away_player_data)
        return game

    def update(self, instance: GameSummary, validated_data: GameSummaryCreate):
        home_players_data = cast(
            list[PlayerOnGameCreate] | None,
            validated_data.pop("home_players_on_game", None),
        )
        away_players_data = cast(
            list[PlayerOnGameCreate] | None,
            validated_data.pop("away_players_on_game", None),
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if home_players_data is not None:
            for home_player_data in home_players_data:
                PlayerOnGame.objects.filter(game_id=instance.game_id, player_id=home_player_data["player_id"]).delete()
                PlayerOnGame.objects.create(game_id=instance, is_home=True, **home_player_data)
        if away_players_data is not None:
            for away_player_data in away_players_data:
                PlayerOnGame.objects.filter(game_id=instance.game_id, player_id=away_player_data["player_id"]).delete()
                PlayerOnGame.objects.create(game_id=instance, is_home=False, **away_player_data)

        return instance

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        errors: dict[str, str] = {}
        if attrs.get("home_team").team_id == attrs.get("away_team").team_id:  # type: ignore
            errors["team_id"] = "Home and away teams must be different."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
