from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.nba_api.GetGameSummariesService import GetGameSummariesService
from ..serializers.nba_api.GameSummarySerializer import GameSummarySerializer


class NBAGameSummariesView(APIView):
    def get(self, request):
        try:
            date_str = request.query_params.get('date')
            if not date_str:
                return Response({'error': 'date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            game_summaries = GetGameSummariesService().get_game_summaries_for_date(date_str)
            return Response(GameSummarySerializer(game_summaries, many=True).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
