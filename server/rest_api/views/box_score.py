from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from box_score_arc.settings import is_dev_mode
from rest_api.models.box_score import BoxScore
from rest_api.serializers.box_score import BoxScoreSerializer
from rest_api.services.box_score_service import fetch_box_scores, upsert_box_score

class BoxScoreViewSet(viewsets.ModelViewSet):
    queryset = BoxScore.objects.all()
    serializer_class = BoxScoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game_id']
    if not is_dev_mode:
        http_method_names = ['get', 'head', 'options']
    
    def list(self, request, *args, **kwargs):
        game_id = request.query_params.get('game_id')
        # MYTODO: #34 対象の試合がライブ中の場合の切り分けはここでする BoxScore にstatus id 属性を追加するか、、
        if game_id is None:
            return super().list(request, *args, **kwargs)
        if BoxScore.objects.filter(game_id=game_id).exists():
            instance = BoxScore.objects.get(game_id=game_id)
        else:
            try:
                box_scores_creates = fetch_box_scores([game_id])
                upsert_box_score(box_scores_creates[0])
                instance = BoxScore.objects.get(game_id=game_id)
            except:
                instance = None
        if instance:
            return Response(self.get_serializer(instance).data)
        else:
            return Response([])



