from django.db import models

class BoxScoreDataForPostgres(models.Model):
    game_id = models.CharField(primary_key=True)
    data = models.JSONField()

    class Meta:
        db_table = "box_score_data"
    
    def upsert(self):
        self.__class__.objects.update_or_create(
            game_id=self.game_id,
            defaults={
                "data": self.data,
            }
        )