import datetime
from ...models.nba_api.BoxScoreDataModel import BoxScoreData
from ...models.postgres.BoxScoreDataForPostgresModel import BoxScoreDataForPostgres
from ..nba_api.BoxScoreDataNbaApiService import BoxScoreDataNbaApiService

class GetBoxScoreDataService:

    def __init__(self, game_id: str, boxScoreDataNbaApiService=None):
        self.game_id = game_id
        self.boxScoreDataNbaApiService = boxScoreDataNbaApiService or BoxScoreDataNbaApiService(game_id=game_id)

    def get_box_score_data(self) -> BoxScoreData:
        start_time = datetime.datetime.now()
        box_score_data_from_postgres = BoxScoreDataForPostgres.objects.filter(game_id=self.game_id).first()
        if box_score_data_from_postgres == None:
            box_score_data_from_nba_api = self.boxScoreDataNbaApiService.get_box_score_data()
            box_score_data_from_nba_api_for_postgres: BoxScoreDataForPostgres = box_score_data_from_nba_api.to_postgres_model()
            box_score_data_from_nba_api_for_postgres.upsert()
            time_diff = (datetime.datetime.now() - start_time).total_seconds()
            print(f"return box score data from nba_api. time: {time_diff}")
            return box_score_data_from_nba_api
        else:
            time_diff = (datetime.datetime.now() - start_time).total_seconds()
            print(f"return box score data from postgres. time: {time_diff}")
            return BoxScoreData.from_postgres_model(box_score_data_from_postgres)


