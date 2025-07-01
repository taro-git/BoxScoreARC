from ...models.nba_api.BoxScoreSummaryModel import BoxScoreSummary
from ...models.postgres.BoxScoreSummaryForPostgresModel import BoxScoreSummaryForPostgres
from ..nba_api.BoxScoreSummaryNbaApiService import BoxScoreSummaryNbaApiService

class GetBoxScoreSummaryService:
    def __init__(self, game_id: str, boxScoreSummaryNbaApiService=None):
        self.game_id = game_id
        self.boxScoreSummaryNbaApiService = boxScoreSummaryNbaApiService or BoxScoreSummaryNbaApiService(game_id=game_id)

    def get_box_score_summary(self):
        box_score_summary_from_postgres = BoxScoreSummaryForPostgres.objects.filter(game_id=self.game_id).first()
        if box_score_summary_from_postgres == None:
            box_score_summary_from_nba_api = self.boxScoreSummaryNbaApiService.get_box_score_summary()
            box_score_summary_from_nba_api_for_postgres: BoxScoreSummaryForPostgres = box_score_summary_from_nba_api.to_postgres_model()
            box_score_summary_from_nba_api_for_postgres.upsert()
            return box_score_summary_from_nba_api
        else:
            return BoxScoreSummary.from_postgres_model(box_score_summary_from_postgres)
