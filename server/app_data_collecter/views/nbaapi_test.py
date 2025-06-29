from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplayv3, playbyplayv2, scoreboardv2, boxscoretraditionalv2, boxscoresummaryv2, boxscoretraditionalv3, boxscoreplayertrackv3
from nba_api.live.nba.endpoints import playbyplay, boxscore


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

            # games = leaguegamefinder.LeagueGameFinder(season_nullable="2024-25", league_id_nullable="00")
            # df_games = pd.DataFrame(games.league_game_finder_results.get_data_frame())  # 過去の試合のゲームサマリーはこれを使う
            # playbyplay3 = playbyplayv3.PlayByPlayV3(game_id="0042400216")
            # df_playbyplay3 = pd.DataFrame(playbyplay3.play_by_play.get_data_frame())
            # df_playbyplay3_tyusyutsu = df_playbyplay3.loc[:, ['period', 'clock', 'teamTricode', 'personId','actionType', 'subType', 'description']]
            playbyplay2 = playbyplayv2.PlayByPlayV2(game_id="0042400401") # 当日の試合でもある　試合中でもあるかは未確認
            df_playbyplay2 = pd.DataFrame(playbyplay2.play_by_play.get_data_frame())   # PlayByPlayV2 を使う　理由は　asisst、steal、blockなどに明示的（笑）にplayerIDがつくから
            # boxScoreSummaryV2 = boxscoresummaryv2.BoxScoreSummaryV2(game_id="0042400304") # 当日の試合でもある　試合中でもあるかは未確認
            # inactive_players = boxScoreSummaryV2.inactive_players.get_data_frame() # インアクティブプレイヤーがわかる
            # game_summary = pd.DataFrame(boxScoreSummaryV2.game_summary.get_data_frame()) # home team id、away team id がわかる
            # line_score = pd.DataFrame(boxScoreSummaryV2.line_score.get_data_frame()) # team ごとの情報がある id 3文字の名前、クウォーターごとの得点
            boxScoreTraditionalV3 = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id="0042400401", end_range="7390", end_period="0", range_type="2", start_range="7200", start_period="0" ) # チームの選手一覧（ボックススコアあるけど不要）
            # print(boxScoreTraditionalV3.player_stats.get_data_frame())
            # player_stats = pd.DataFrame(boxScoreTraditionalV2.player_stats.get_data_frame())
            # boxScore = boxscore.BoxScore(game_id="0042400304") # 当日のデータも試合終わっちゃってるとない
            # df_boxScore = pd.DataFrame(boxScore.home_team.get_data_frame())
            # liveplaybyplay = playbyplay.PlayByPlay(game_id="0042400304") # 当日のデータも試合終わっちゃってるとない
            # df_liveplaybyplay = pd.DataFrame(liveplaybyplay.actions.get_data_frame()) 
            # print(df_games)
            # print(df_playbyplay2[df_playbyplay2["EVENTMSGTYPE"] == 9][["EVENTMSGACTIONTYPE","SCORE", "PERIOD","PCTIMESTRING","HOMEDESCRIPTION", "NEUTRALDESCRIPTION", "VISITORDESCRIPTION","PLAYER1_ID" ,"PLAYER1_NAME", "PLAYER2_NAME", "PLAYER3_NAME"]])
            # print(df_playbyplay2[df_playbyplay2["EVENTMSGTYPE"] == 8])
            print(df_playbyplay2)
            # print(df_liveplaybyplay)
            # print(inactive_players)
            # print(game_summary)
            # print(line_score)
            # print(player_stats) # スターターの START_POSITION のみに値が入っているケースが多い。見分けつかなかったら上から表示しちゃえばいいと思う。
            # print(player_stats.loc[:, ['teamId', 'personId', 'nameI', 'position', 'jerseyNum']])
            # print(list(df.columns))
            # print(df_out)
            # print(df_playbyplay3.loc[:, 'description'].unique())
            # print(df.iloc[38])
            # 2024-25 0042400216
            # 2019-20 0021900917
            # 2010-11 0021000294
            # 2000-01 0020000905




            return Response(df_playbyplay2.to_json(orient="records", indent=2), status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
