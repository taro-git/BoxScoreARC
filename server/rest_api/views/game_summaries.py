from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from box_score_arc.settings import is_dev_mode
from rest_api.models.game_summary import GameSummary
from rest_api.serializers.game_summary import GameSummarySerializer

class GameSummariesViewSet(viewsets.ModelViewSet):
    queryset = GameSummary.objects.all()
    serializer_class = GameSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game_id', 'game_date_est', 'home_team_id', 'away_team_id']
    if not is_dev_mode:
        http_method_names = ['get', 'head', 'options'] 
