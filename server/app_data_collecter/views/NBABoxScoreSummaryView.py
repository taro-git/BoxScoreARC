from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..services.nba_api.BoxScoreSummaryNbaApiService import BoxScoreSummaryNbaApiService
from ..serializers.nba_api.BoxScoreSummarySerializer import BoxScoreSummarySerializer


class NBABoxScoreSummaryView(APIView):
    def get(self, request):
        try:
            game_id = request.query_params.get('gameId')
            if not game_id:
                return Response({'error': 'gameId parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            box_score_summary = BoxScoreSummaryNbaApiService().get_box_score_summary(game_id)
            return Response(BoxScoreSummarySerializer(box_score_summary).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
