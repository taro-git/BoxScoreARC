from django.urls import path
from .views.clickhouse_test import clickhouse_test
from .views.nbaapi_test import NBAGamesView

urlpatterns = [
    path('api/clickhouse-test/', clickhouse_test),
    path('api/nbaapi-test/', NBAGamesView.as_view()),
]
