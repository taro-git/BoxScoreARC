from rest_framework import viewsets

from box_score_arc.settings import is_dev_mode
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus
from rest_api.serializers.scheduled_box_score_status import (
    ScheduledBoxScoreStatusSerializer,
)


class ScheduledBoxScoreStatusViewSet(viewsets.ModelViewSet):
    queryset = ScheduledBoxScoreStatus.objects.all()
    serializer_class = ScheduledBoxScoreStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["game_id"]
    if not is_dev_mode:
        http_method_names = ["get", "head", "options", "post"]
