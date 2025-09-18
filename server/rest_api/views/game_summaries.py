from rest_framework import viewsets

import django_filters
from box_score_arc.settings import is_dev_mode
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.models.game_summary import GameSummary
from rest_api.serializers.game_summary import GameSummarySerializer


class GameSummaryFilter(django_filters.FilterSet):
    game_datetime = django_filters.DateFilter(field_name="game_datetime", lookup_expr="date")

    class Meta:
        model = GameSummary
        fields = ["game_id", "game_datetime", "home_team_id", "away_team_id"]


class GameSummariesViewSet(viewsets.ModelViewSet):
    queryset = GameSummary.objects.all()
    serializer_class = GameSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameSummaryFilter
    if not is_dev_mode:
        http_method_names = ["get", "head", "options"]
