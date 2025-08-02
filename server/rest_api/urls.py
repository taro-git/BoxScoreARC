from rest_framework import routers

from rest_api.views.game_summaries import GameSummariesViewSet
from rest_api.views.box_score import BoxScoreViewSet

router = routers.DefaultRouter()
router.register('game_summaries', GameSummariesViewSet)
router.register('box_score', BoxScoreViewSet)

urlpatterns = router.urls
