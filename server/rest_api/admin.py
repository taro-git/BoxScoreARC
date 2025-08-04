from django.contrib import admin

from rest_api.models.game_summary import GameSummary, Team, PlayerOnGame
from rest_api.models.box_score import BoxScore, BoxScorePlayer, BoxScoreData
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus

@admin.register(GameSummary)
class GameSummary(admin.ModelAdmin):
    pass

@admin.register(Team)
class Team(admin.ModelAdmin):
    pass

@admin.register(PlayerOnGame)
class PlayerOnGame(admin.ModelAdmin):
    pass


@admin.register(BoxScore)
class BoxScore(admin.ModelAdmin):
    pass

@admin.register(BoxScorePlayer)
class BoxScorePlayer(admin.ModelAdmin):
    pass

@admin.register(BoxScoreData)
class BoxScoreData(admin.ModelAdmin):
    pass

@admin.register(ScheduledBoxScoreStatus)
class ScheduledBoxScoreStatus(admin.ModelAdmin):
    pass
