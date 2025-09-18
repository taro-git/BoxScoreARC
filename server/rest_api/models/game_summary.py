from django.db import models


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField()
    logo = models.CharField()


class GameSummary(models.Model):
    game_id = models.CharField(primary_key=True)
    sequence = models.IntegerField()
    status_id = models.IntegerField()
    """1: scheduled, 2: game started, 3: game finished"""
    status_text = models.CharField()
    game_datetime = models.DateTimeField()
    """サマータイム考慮のニューヨーク時間"""
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="home_games")
    home_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="away_games")
    away_score = models.IntegerField()

    @property
    def home_players_on_game(self) -> list["PlayerOnGame"]:
        return self.players.filter(is_home=True)  # type: ignore

    @property
    def away_players_on_game(self) -> list["PlayerOnGame"]:
        return self.players.filter(is_home=False)  # type: ignore

    @property
    def game_category(self) -> str:
        return {
            "1": "Preseason",
            "2": "Regular Season",
            "3": "All Star",
            "4": "Playoffs",
            "5": "Play-In Tournament",
            "6": "Emirates NBA Cup",
        }.get(self.game_id[2], "Unknown")

    @property
    def season(self):
        year = int(self.game_id[3:5])
        year = 2000 + year if year < 80 else 1900 + year
        return f"{year}-{(year + 1) % 100:02d}"


class PlayerOnGame(models.Model):
    game_id = models.ForeignKey(GameSummary, on_delete=models.CASCADE, related_name="players")
    is_home = models.BooleanField()
    player_id = models.IntegerField()
    name = models.CharField()
    jersey = models.CharField(null=True, blank=True)
    position = models.CharField(null=True, blank=True)
    is_starter = models.BooleanField()
    is_inactive = models.BooleanField()
    sequence = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game_id", "player_id"],
                name="unique_game_summary_game_id_player_id",
            )
        ]
