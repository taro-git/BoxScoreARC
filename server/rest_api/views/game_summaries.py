from rest_framework import viewsets
from rest_framework.response import Response
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from box_score_arc.settings import is_dev_mode
from rest_api.models.game_summary import GameSummary
from rest_api.serializers.game_summary import GameSummarySerializer
from rest_api.services.game_summary_service import update_players_in_game_summary_by_game_id, upsert_game_summary


class GameSummaryFilter(django_filters.FilterSet):
    game_datetime = django_filters.DateFilter(field_name="game_datetime", lookup_expr="date")

    class Meta:
        model = GameSummary
        fields = ['game_id', 'game_datetime', 'home_team_id', 'away_team_id']


class GameSummariesViewSet(viewsets.ModelViewSet):
    queryset = GameSummary.objects.all()
    serializer_class = GameSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameSummaryFilter
    if not is_dev_mode:
        http_method_names = ['get', 'head', 'options'] 
    
    def list(self, request, *args, **kwargs):
        game_id = request.query_params.get('game_id')
        if game_id is None:
            game_summaries_response = super().list(request, *args, **kwargs)
            # MYTODO: #34 game_summaries のうち、live（status_id==2）のものは更新が効くようにする
            return game_summaries_response
        if GameSummary.objects.filter(game_id=game_id).exists():
            game_summary_create = update_players_in_game_summary_by_game_id(game_id)
            upsert_game_summary(game_summary_create)
            instance = GameSummary.objects.get(game_id=game_id)
            return Response(self.get_serializer(instance).data)
        else:
            return Response([])
