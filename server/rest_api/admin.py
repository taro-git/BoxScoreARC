from django.contrib import admin

from .models.game_summary import GameSummary, TeamOnGame, PlayerOnGame

@admin.register(GameSummary)
class GameSummary(admin.ModelAdmin):
    pass

@admin.register(TeamOnGame)
class TeamOnGame(admin.ModelAdmin):
    pass

@admin.register(PlayerOnGame)
class PlayerOnGame(admin.ModelAdmin):
    pass
