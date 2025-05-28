from django.urls import path

from .views.nbaapi_test import NBAApiTest
from .views.clickhouse_test import clickhouse_test
from .views.NBAGameSummariesView import NBAGameSummariesView
from .views.NBABoxScoreSummaryView import NBABoxScoreSummaryView

urlpatterns = [
    path('api/clickhouse-test/', clickhouse_test),
    path('api/nba/game-summaries/', NBAGameSummariesView.as_view()),
    path('api/nba/box-score-summary/', NBABoxScoreSummaryView.as_view()),
    path('api/nbaapi-test/', NBAApiTest.as_view()),
]
