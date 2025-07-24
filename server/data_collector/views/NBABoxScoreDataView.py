from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.common.GetBoxScoreDataService import GetBoxScoreDataService
from ..serializers.nba_api.BoxScoreDataSerializer import BoxScoreDataSerializer

class NBABoxScoreDataView(APIView):
    def get(self, request):
        try:
            game_id = request.query_params.get('gameId')
            if not game_id:
                return Response({'error': 'gameId parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            box_score_data = GetBoxScoreDataService(game_id=game_id).get_box_score_data()
            return Response(BoxScoreDataSerializer(box_score_data).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
