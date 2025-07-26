from django.contrib import admin

from .models.game_summary import GameSummary, Team, PlayerOnGame

@admin.register(GameSummary)
class GameSummary(admin.ModelAdmin):
    pass

@admin.register(Team)
class Team(admin.ModelAdmin):
    pass

@admin.register(PlayerOnGame)
class PlayerOnGame(admin.ModelAdmin):
    pass
