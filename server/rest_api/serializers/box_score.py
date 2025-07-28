from rest_framework import serializers

from ..models.box_score import BoxScore, BoxScorePlayer, BoxScoreData


class BoxScoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxScoreData
        exclude = ['id', 'player']


class BoxScorePlayerSerializer(serializers.ModelSerializer):
    box_score_data = BoxScoreDataSerializer(many=True, source='data')
    class Meta:
        model = BoxScorePlayer
        fields = ['player_id', 'box_score_data']


class BoxScoreSerializer(serializers.ModelSerializer):
    home_players = BoxScorePlayerSerializer(many=True, source='home_players_on_box_score')
    away_players = BoxScorePlayerSerializer(many=True, source='away_players_on_box_score')
    class Meta:
        model = BoxScore
        fields = '__all__'
    
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
