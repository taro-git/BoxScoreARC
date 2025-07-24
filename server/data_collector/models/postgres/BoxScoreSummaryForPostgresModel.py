from django.db import models

class BoxScoreSummaryForPostgres(models.Model):
    game_id = models.CharField(primary_key=True)
    game_date_jst = models.DateField()
    home = models.JSONField()
    away = models.JSONField()

    class Meta:
        db_table = "box_score_summary"
    
    def upsert(self):
        self.__class__.objects.update_or_create(
            game_id=self.game_id,
            defaults={
                "game_date_jst": self.game_date_jst,
                "home": self.home,
                "away": self.away,
            }
        )