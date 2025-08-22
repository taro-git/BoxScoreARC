from rest_framework import routers

from rest_api.views.game_summaries import GameSummariesViewSet
from rest_api.views.box_score import BoxScoreViewSet
from rest_api.views.scheduled_box_score_status import ScheduledBoxScoreStatusViewSet
from rest_api.views.season_summary import SeasonSummaryViewSet

router = routers.DefaultRouter()
router.register('game_summaries', GameSummariesViewSet)
router.register('box_score', BoxScoreViewSet)
router.register('scheduled_box_score_status', ScheduledBoxScoreStatusViewSet)
router.register('season_summaries', SeasonSummaryViewSet)

urlpatterns = router.urls
