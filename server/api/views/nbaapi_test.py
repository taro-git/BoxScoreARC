from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplayv3, playbyplayv2, playbyplay, scoreboardv2
from ..models.clickhouse.GameSummaryForClickhouseModel import GameSummaryForClickhouse
from ..services.clickhouse.GameSummariesClickhouseService import GameSummariesClickhouseService


class NBAApiTest(APIView):
    def get(self, request):
        try:
            date_str = request.query_params.get('date')
            if not date_str:
                return Response({'error': 'date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
            pd.set_option('display.max_rows', None)        # 行をすべて表示
            pd.set_option('display.max_columns', None)     # 列をすべて表示
            pd.set_option('display.width', None)           # 横幅による折返しを防止
            pd.set_option('display.max_colwidth', None)    # 各列の内容の最大文字数

            games = leaguegamefinder.LeagueGameFinder(season_nullable="2024-25", league_id_nullable="00")
            df_games = pd.DataFrame(games.league_game_finder_results.get_data_frame())  # 過去の試合のゲームサマリーはこれを使う
            playbyplay3 = playbyplayv3.PlayByPlayV3(game_id="0042400216")
            df_playbyplay3 = pd.DataFrame(playbyplay3.play_by_play.get_data_frame())
            df_playbyplay3_tyusyutsu = df_playbyplay3.loc[:, ['period', 'clock', 'teamTricode', 'personId','actionType', 'subType', 'description']]
            playbyplay2 = playbyplayv2.PlayByPlayV2(game_id="0020000905")
            df_playbyplay2 = pd.DataFrame(playbyplay2.play_by_play.get_data_frame())   # PlayByPlayV2 を使う　理由は　asisst、steal、blockなどに明示的（笑）にplayerIDがつくから
            playbyplay1 = playbyplay.PlayByPlay(game_id="0042400216")
            df_playbyplay1 = pd.DataFrame(playbyplay1.play_by_play.get_data_frame())
            # print(df_games)
            # print(df_playbyplay2)
            # print(list(df.columns))
            # print(df_out)
            # print(df_playbyplay3.loc[:, 'description'].unique())
            # print(df.iloc[38])
            # 2024-25 0042400216
            # 2019-20 0021900917
            # 2010-11 0021000294
            # 2000-01 0020000905

            # game_summaries_for_clickhouse = GameSummaryForClickhouse(
            #     game_id='0022400174',
            #     home_team='MEM',
            #     home_score=131,
            #     away_team='LAL',
            #     away_score=114,
            #     game_sequence=6,
            #     status_id=3,
            #     status_text='Final',
            #     live_period=4,
            #     live_clock='00:00',
            #     game_date_jst='2024-11-07'
            # )

            # test_clickhouse = GameSummariesClickhouseService(table_name='test')
            # test_clickhouse.upsert_game_summaries([game_summaries_for_clickhouse])
            # print(test_clickhouse.get_game_summaries())




            return Response(df_games.to_json(orient="records", indent=2), status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
