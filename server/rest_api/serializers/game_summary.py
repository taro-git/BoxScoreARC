from typing import TypedDict, List
from datetime import datetime

from rest_framework import serializers

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
    home_players: List[PlayerOnGameCreate]
    away_players: List[PlayerOnGameCreate]

##
## Serializer
#### 
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerOnGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerOnGame
        fields = ['player_id', 'name', 'jersey', 'position', 'is_starter', 'is_inactive', 'sequence']


class GameSummarySerializer(serializers.ModelSerializer):
    home_players = PlayerOnGameSerializer(many=True, source='home_players_on_game')
    away_players = PlayerOnGameSerializer(many=True, source='away_players_on_game')
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    home_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='home_team', write_only=True
    )
    away_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='away_team', write_only=True
    )

    class Meta:
        model = GameSummary
        fields = '__all__'

    def create(self, validated_data):
        home_players_data = validated_data.pop('home_players_on_game', [])
        away_players_data = validated_data.pop('away_players_on_game', [])
        game = GameSummary.objects.create(**validated_data)
        for home_player_data in home_players_data:
            PlayerOnGame.objects.create(game_id=game, is_home=True, **home_player_data)
        for away_player_data in away_players_data:
            PlayerOnGame.objects.create(game_id=game, is_home=False, **away_player_data)
        return game

    def update(self, instance, validated_data):
        home_players_data = validated_data.pop('home_players_on_game', None)
        away_players_data = validated_data.pop('away_players_on_game', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if home_players_data is not None:
            instance.players.filter(is_home=True).delete()
            for home_player_data in home_players_data:
                PlayerOnGame.objects.create(game_id=instance, is_home=True, **home_player_data)
        if away_players_data is not None:
            instance.players.filter(is_home=False).delete()
            for away_player_data in away_players_data:
                PlayerOnGame.objects.create(game_id=instance, is_home=False, **away_player_data)

        return instance

    def validate(self, data):
        errors = {}
        if data.get('home_team').team_id == data.get('away_team').team_id:
            errors['team_id'] = "Home and away teams must be different."
        if errors:
            raise serializers.ValidationError(errors)
        return data
