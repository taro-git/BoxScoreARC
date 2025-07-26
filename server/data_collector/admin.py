from django.contrib import admin

from .models.postgres.BoxScoreDataForPostgresModel import BoxScoreDataForPostgres
from .models.postgres.BoxScoreSummaryForPostgresModel import BoxScoreSummaryForPostgres
from .models.postgres.GameSummaryForPostgresModel import GameSummaryForPostgres
from .models.postgres.SeasonRangeForPostgresModel import SeasonRangeForPostgres


@admin.register(BoxScoreDataForPostgres)
class BoxScoreDataForPostgres(admin.ModelAdmin):
    pass

@admin.register(BoxScoreSummaryForPostgres)
class BoxScoreSummaryForPostgres(admin.ModelAdmin):
    pass

@admin.register(GameSummaryForPostgres)
class GameSummaryForPostgres(admin.ModelAdmin):
    pass

@admin.register(SeasonRangeForPostgres)
class SeasonRangeForPostgres(admin.ModelAdmin):
    pass
