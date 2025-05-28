from rest_framework import serializers

class PlayerSerializer(serializers.Serializer):
    player_id = serializers.IntegerField()
    name = serializers.CharField()
    position = serializers.CharField()
    is_inactive = serializers.BooleanField()
    sequence = serializers.IntegerField()


class TeamSummarySerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    abbreviation = serializers.CharField()
    logo = serializers.CharField(read_only=True)
    players = PlayerSerializer(many=True)


class BoxScoreSummarySerializer(serializers.Serializer):
    game_date_jst = serializers.DateField()
    home = TeamSummarySerializer()
    away = TeamSummarySerializer()
