from django.urls import path
from .views.clickhouse_test import clickhouse_test
from .views.NBAGameSummariesView import NBAGameSummariesView

urlpatterns = [
    path('api/clickhouse-test/', clickhouse_test),
    path('api/nba/game-summaries/', NBAGameSummariesView.as_view()),
]
