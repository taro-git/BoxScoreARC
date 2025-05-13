from django.urls import path
from .views import clickhouse_test

urlpatterns = [
    path('clickhouse-test/', clickhouse_test),
]
