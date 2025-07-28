from rest_framework import routers

from .views.game_summaries import GameSummariesViewSet
from .views.box_score import BoxScoreViewSet

router = routers.DefaultRouter()
router.register('game_summaries', GameSummariesViewSet)
router.register('box_score', BoxScoreViewSet)

urlpatterns = router.urls
