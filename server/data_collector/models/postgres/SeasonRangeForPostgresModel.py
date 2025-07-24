from django.db import models

class SeasonRangeForPostgres(models.Model):
    season = models.CharField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    update_game_summaries_date = models.DateField()

    class Meta:
        db_table = "season_ranges"
    
    def upsert(self):
        self.__class__.objects.update_or_create(
            season=self.season,
            defaults={
                "start_date": self.start_date,
                "end_date": self.end_date,
                "update_game_summaries_date": self.update_game_summaries_date
            }
        )