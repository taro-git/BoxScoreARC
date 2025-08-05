from typing import TypedDict, List

from rest_framework import serializers

from rest_api.models.box_score import BoxScore, BoxScorePlayer, BoxScoreData

##
## schema for access from django self
#### 
class BoxScoreDataCreate(TypedDict):
    elapsed_seconds: int
    is_on_court: bool
    sec: int
    pts: int
    reb: int
    ast: int
    stl: int
    blk: int
    fg: int
    fga: int
    three: int
    threea: int
    ft: int
    fta: int
    oreb: int
    dreb: int
    to: int
    pf: int
    plusminus: int


class PlayerOnBoxScoreCreate(TypedDict):
    player_id: int
    box_score_data: List[BoxScoreDataCreate]


class BoxScoreCreate(TypedDict):
    game_id: int
    final_seconds: int
    """ゲーム終了時点の経過時間 (秒)"""
    home_players: List[PlayerOnBoxScoreCreate]
    away_players: List[PlayerOnBoxScoreCreate]


##
## Serializer
#### 
BOX_SCORE_HEADER = [
    'elapsed_seconds',
    'is_on_court',
    'min',
    'pts',
    'reb',
    'ast',
    'stl',
    'blk',
    'fg',
    'fga',
    'three',
    'threea',
    'ft',
    'fta',
    'oreb',
    'dreb',
    'to',
    'pf',
    'eff',
    'plusminus',
]

def _snake_to_camel(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class BoxScoreDataSerializer(serializers.ModelSerializer):
    sec = serializers.IntegerField(write_only=True)
    min = serializers.SerializerMethodField()
    eff = serializers.SerializerMethodField()

    class Meta:
        model = BoxScoreData
        exclude = ['id', 'player']
    
    def get_min(self, obj):
        return obj.min
    
    def get_eff(self, obj):
        return obj.eff
    
    def to_representation(self, instance):
        return [getattr(instance, header) for header in BOX_SCORE_HEADER]


class BoxScorePlayerSerializer(serializers.ModelSerializer):
    box_score_data = BoxScoreDataSerializer(many=True, source='data')
    class Meta:
        model = BoxScorePlayer
        fields = ['player_id', 'box_score_data']


class BoxScoreSerializer(serializers.ModelSerializer):
    final_seconds = serializers.IntegerField(write_only=True)
    final_period = serializers.SerializerMethodField()
    is_collect = serializers.SerializerMethodField()
    box_score_data_header = serializers.SerializerMethodField()
    home_players = BoxScorePlayerSerializer(many=True, source='home_players_on_box_score')
    away_players = BoxScorePlayerSerializer(many=True, source='away_players_on_box_score')
    class Meta:
        model = BoxScore
        fields = '__all__'
    
    def get_final_period(self, obj):
        return obj.final_period
    
    def get_is_collect(self, obj):
        return obj.is_collect
    
    def get_box_score_data_header(self, obj):
        return [_snake_to_camel(snake_str) for snake_str in BOX_SCORE_HEADER]
    
    def _create_player_and_data(self, box_score: BoxScore, players_data: list, is_home: bool):
        for player_data in players_data:
            moments_data = player_data.pop('data', [])
            box_score_player = BoxScorePlayer.objects.create(game_id=box_score, is_home=is_home, **player_data)
            for moment_data in moments_data:
                BoxScoreData.objects.create(player=box_score_player, **moment_data) 

    def create(self, validated_data):
        home_players_data = validated_data.pop('home_players_on_box_score', [])
        away_players_data = validated_data.pop('away_players_on_box_score', [])
        box_score = BoxScore.objects.create(**validated_data)
        self._create_player_and_data(box_score, home_players_data, True)
        self._create_player_and_data(box_score, away_players_data, False)
        return box_score

    def update(self, instance, validated_data):
        home_players_data = validated_data.pop('home_players_on_box_score', None)
        away_players_data = validated_data.pop('away_players_on_box_score', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if home_players_data is not None:
            instance.players.filter(is_home=True).delete()
            self._create_player_and_data(instance, home_players_data, True)
        if away_players_data is not None:
            instance.players.filter(is_home=False).delete()
            self._create_player_and_data(instance, away_players_data, False)

        return instance
