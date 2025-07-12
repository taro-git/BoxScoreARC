from django.urls import path

from .views.nbaapi_test import NBAApiTest
from .views.clickhouse_test import clickhouse_test
from .views.NBAGameSummariesView import NBAGameSummariesView
from .views.NBABoxScoreSummaryView import NBABoxScoreSummaryView
from .views.NBABoxScoreDataView import NBABoxScoreDataView

urlpatterns = [
    path('api/v1/clickhouse-test/', clickhouse_test),
    path('api/v1/nba/game-summaries/', NBAGameSummariesView.as_view()),
    path('api/v1/nba/box-score-summary/', NBABoxScoreSummaryView.as_view()),
    path('api/v1/nba/box-score-data/', NBABoxScoreDataView.as_view()),
    path('api/v1/nbaapi-test/', NBAApiTest.as_view()),
]
