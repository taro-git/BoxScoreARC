from django.db import models

class GameSummaryForPostgres(models.Model):
    game_id = models.CharField(primary_key=True)
    home_team = models.CharField()
    home_score = models.IntegerField()
    away_team = models.CharField()
    away_score = models.IntegerField()
    game_sequence = models.IntegerField()
    status_id = models.IntegerField()
    status_text = models.CharField()
    live_period = models.IntegerField()
    live_clock = models.CharField()
    game_date_jst = models.DateField()

    class Meta:
        db_table = "game_summaries"
    
    def upsert(self):
        self.__class__.objects.update_or_create(
            game_id=self.game_id,
            defaults={
                "home_team": self.home_team,
                "home_score": self.home_score,
                "away_team": self.away_team,
                "away_score": self.away_score,
                "game_sequence": self.game_sequence,
                "status_id": self.status_id,
                "status_text": self.status_text,
                "live_period": self.live_period,
                "live_clock": self.live_clock,
                "game_date_jst": self.game_date_jst
            }
        )