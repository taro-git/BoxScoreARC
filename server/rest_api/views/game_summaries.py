from rest_framework import viewsets, filters

from rest_api.models.game_summary import GameSummary
from rest_api.serializers.game_summary import GameSummarySerializer

class GameSummariesViewSet(viewsets.ModelViewSet):
    queryset = GameSummary.objects.all()
    serializer_class = GameSummarySerializer
