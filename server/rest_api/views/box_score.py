from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from box_score_arc.settings import is_dev_mode
from rest_api.models.box_score import BoxScore
from rest_api.serializers.box_score import BoxScoreSerializer
from rest_api.services.box_score_service import fetch_box_score, upsert_box_score

class BoxScoreViewSet(viewsets.ModelViewSet):
    queryset = BoxScore.objects.all()
    serializer_class = BoxScoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game_id']
    if not is_dev_mode:
        http_method_names = ['get', 'head', 'options']



