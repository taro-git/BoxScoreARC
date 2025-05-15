from rest_framework import serializers

class GameSummarySerializer(serializers.Serializer):
    game_id = serializers.CharField()
    home_team = serializers.CharField()
    home_score = serializers.IntegerField()
    away_team = serializers.CharField()
    away_score = serializers.IntegerField()
    game_sequence = serializers.IntegerField()
    status_id = serializers.IntegerField()
    status_text = serializers.CharField()
    live_period = serializers.IntegerField()
    live_clock = serializers.CharField()
