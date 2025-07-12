from django.urls import path

from .views.nbaapi_test import NBAApiTest
from .views.clickhouse_test import clickhouse_test
from .views.NBAGameSummariesView import NBAGameSummariesView
from .views.NBABoxScoreSummaryView import NBABoxScoreSummaryView
from .views.NBABoxScoreDataView import NBABoxScoreDataView

urlpatterns = [
    path('clickhouse-test/', clickhouse_test),
    path('nba/game-summaries/', NBAGameSummariesView.as_view()),
    path('nba/box-score-summary/', NBABoxScoreSummaryView.as_view()),
    path('nba/box-score-data/', NBABoxScoreDataView.as_view()),
    path('nbaapi-test/', NBAApiTest.as_view()),
]
