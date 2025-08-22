from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from box_score_arc.settings import is_dev_mode
from rest_api.models.season_summary import SeasonSummary
from rest_api.serializers.season_summary import SeasonSummarySerializer

class SeasonSummaryViewSet(viewsets.ModelViewSet):
    queryset = SeasonSummary.objects.all()
    serializer_class = SeasonSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['season']
    if not is_dev_mode:
        http_method_names = ['get', 'head', 'options']



