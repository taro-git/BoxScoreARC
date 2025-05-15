from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.nba_api.GetNBAGamesService import get_games


class NBAGamesView(APIView):
    def get(self, request):
        try:
            date_str = request.query_params.get('date')
            if not date_str:
                return Response({'error': 'date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            games = get_games(date_str)
            return Response(games, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
