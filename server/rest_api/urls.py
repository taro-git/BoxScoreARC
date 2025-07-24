from rest_framework import routers

from .views.game_summaries import GameSummariesViewSet

router = routers.DefaultRouter()
router.register('game_summaries', GameSummariesViewSet)

urlpatterns = router.urls
