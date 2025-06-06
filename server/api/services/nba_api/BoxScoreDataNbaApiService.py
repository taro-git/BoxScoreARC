import re
from types import SimpleNamespace
from nba_api.stats.endpoints import playbyplayv2

from ...models.nba_api.BoxScoreDataModel import BoxScoreData
from .BoxScoreSummaryNbaApiService import BoxScoreSummaryNbaApiService

ALLOWED_KEYS: SimpleNamespace = SimpleNamespace(
    MIN=0, PTS=1, REB=2, AST=3, STL=4, BLK=5, FG=6, FGA=7, FG_PCT=8,
    THREEP=9, THREEPA=10, THREE_PCT=11, FT=12, FTA=13, FT_PCT=14,
    OREB=15, DREB=16, TO=17, PF=18, EFF=19, PLUS_MINUS=20
)

class BoxScoreDataNbaApiService:
    
    def __init__(self):
        self.box_score_data = BoxScoreData()
    
    def get_box_score_data(self, game_id: str) -> BoxScoreData:
        play_by_play_v2 = playbyplayv2.PlayByPlayV2(game_id=game_id)
        play_by_play = play_by_play_v2.play_by_play.get_data_frame()
        # あとは playbyplay を BoxScoreData に変換するだけ
        # EVENTMSGTYPE でプレーが区別できる
        # 個人ではなく、チーム単位の事象は PLAYER_ID が TEAM_ID になる
        # 1: フィールドゴール成功 SCORE がNONE じゃなくなる "54 - 54" の形式、PLAYER1_ID が得点、PLAYER2_ID がアシスト（なければPLAYER2_ID は 0）
        # 2: フィールドゴール失敗 PLAYER1_ID がシュートアテンプト、PLAYER3_ID がブロック（なければ 0）
        # 3: フリースロー成功or失敗 失敗のとき SCORE がNONE、成功のとき"54 - 54" の形式、PLAYER1_ID がアテンプト
        # 4: リバウンド PLAYER1_ID が獲得、オフェンスorディフェンスは累積がわかる（HOMEDESCRIPTION か VISITORDESCRIPTION が "Hart REBOUND (Off:1 Def:2)" の形式で他方は必ず None）
        # 5: ターンオーバー PLAYER1_ID がターンオーバー、PLAYER2_ID がスティール（なければ 0）、オフェンスファウルも入っている
        # 6: ファウル PLAYER1_ID がした人、PLAYER2_ID がされた人
        # 7: ターンオーバーを伴わないバイオレーション（キックボール、遅延行為？等） PLAYER1_ID がした人
        # 8: 選手交代 PLAYER1_ID が出てて下がる選手、PLAYER2_ID がベンチから出る選手
        # 9: タイムアウト PLAYER1_ID が申請したチーム
        # 10: ティップオフ PLAYER1_ID がホーム側のジャンパー、PLAYER2_ID がアウェイ側のジャンパー、PLAYER3_ID がボール取った人
        # 11: 退場 多分 PLAYER1_ID が退場になる
        # 12: ピリオドの開始
        # 13: ピリオドの終了
        # 14: データなし
        # 15: データなし
        # 16: データなし
        # 17: データなし
        # 18: チャレンジによるインスタントリプレイ 同じゲームクロックでタイムアウトのチームが申請
        last_score = '0 - 0'
        last_elapsed_seconds = 0
        # MYTODO min と +/- が正しくない⇒おそらくクウォーター間の交代が playbyplay に反映されないことが原因。nba_api の仕様上対応不可能かもしれない
        box_score_summary = BoxScoreSummaryNbaApiService().get_box_score_summary(game_id)
        on_court_away_player_id = [box_score_summary.away.players[i].player_id for i in range(5)]
        on_court_home_player_id = [box_score_summary.home.players[i].player_id for i in range(5)]
        for one_play in play_by_play.itertuples():
            elapsed_seconds = self._get_elapsed_seconds(one_play.PERIOD, one_play.PCTIMESTRING)
            score_diff = self._calc_score_diff(one_play.SCORE, last_score)
            for player_id in on_court_away_player_id + on_court_home_player_id:
                self._append_box_score(player_id, elapsed_seconds, {
                    ALLOWED_KEYS.MIN: elapsed_seconds - last_elapsed_seconds
                })
            match one_play.EVENTMSGTYPE:
                case 1:
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.PTS: score_diff,
                        ALLOWED_KEYS.FG: 1,
                        ALLOWED_KEYS.FGA: 1,
                        ALLOWED_KEYS.THREEP: score_diff - 2,
                        ALLOWED_KEYS.THREEPA: score_diff - 2,
                        ALLOWED_KEYS.EFF: score_diff,
                    })
                    if one_play.PLAYER2_ID != 0:
                        self._append_box_score(one_play.PLAYER2_ID, elapsed_seconds, {
                            ALLOWED_KEYS.AST: 1,
                            ALLOWED_KEYS.EFF: 1,
                        })
                    if one_play.PLAYER1_ID in on_court_away_player_id:
                        for away_player_id in on_court_away_player_id:
                            self._append_box_score(away_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: score_diff,
                            })
                        for home_player_id in on_court_home_player_id:
                            self._append_box_score(home_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: -score_diff,
                            })
                    else:
                        for home_player_id in on_court_home_player_id:
                            self._append_box_score(home_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: score_diff,
                            })
                        for away_player_id in on_court_away_player_id:
                            self._append_box_score(away_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: -score_diff,
                            })
                case 2:
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.FGA: 1,
                        ALLOWED_KEYS.THREEPA: 1 if self._contains_3pt(one_play.HOMEDESCRIPTION, one_play.VISITORDESCRIPTION) else 0,
                        ALLOWED_KEYS.EFF: -1,
                    })
                    if one_play.PLAYER3_ID != 0:
                        self._append_box_score(one_play.PLAYER3_ID, elapsed_seconds, {
                            ALLOWED_KEYS.BLK: 1,
                            ALLOWED_KEYS.EFF: 1,
                        })
                    pass
                case 3:
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.PTS: score_diff,
                        ALLOWED_KEYS.FT: score_diff,
                        ALLOWED_KEYS.FTA: 1,
                        ALLOWED_KEYS.EFF: score_diff + (score_diff - 1)
                    })
                    if one_play.PLAYER1_ID in on_court_away_player_id:
                        for away_player_id in on_court_away_player_id:
                            self._append_box_score(away_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: score_diff,
                            })
                        for home_player_id in on_court_home_player_id:
                            self._append_box_score(home_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: -score_diff,
                            })
                    else:
                        for home_player_id in on_court_home_player_id:
                            self._append_box_score(home_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: score_diff,
                            })
                        for away_player_id in on_court_away_player_id:
                            self._append_box_score(away_player_id, elapsed_seconds, {
                                ALLOWED_KEYS.PLUS_MINUS: -score_diff,
                            })
                case 4:
                    cumulative_reb = self._extract_off_def(one_play.HOMEDESCRIPTION, one_play.VISITORDESCRIPTION)
                    player_last_data = self.box_score_data.data[one_play.PLAYER1_ID][-1][1] if self.box_score_data.data[one_play.PLAYER1_ID] else [0] * len(vars(ALLOWED_KEYS))
                    last_cumulative_reb = {'off': player_last_data[ALLOWED_KEYS.OREB], 'def': player_last_data[ALLOWED_KEYS.DREB]}
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.REB: 1,
                        ALLOWED_KEYS.OREB: cumulative_reb['off'] - last_cumulative_reb['off'],
                        ALLOWED_KEYS.DREB: cumulative_reb['def'] - last_cumulative_reb['def'],
                        ALLOWED_KEYS.EFF: 1,
                    })
                case 5:
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.TO: 1,
                        ALLOWED_KEYS.EFF: -1,
                    })
                    if one_play.PLAYER2_ID != 0:
                        self._append_box_score(one_play.PLAYER2_ID, elapsed_seconds, {
                            ALLOWED_KEYS.STL: 1,
                            ALLOWED_KEYS.EFF: 1,
                        })
                case 6:
                    self._append_box_score(one_play.PLAYER1_ID, elapsed_seconds, {
                        ALLOWED_KEYS.PF: 1
                    })
                case 8:
                    try: 
                        if one_play.PLAYER1_ID in on_court_away_player_id:
                            on_court_away_player_id.remove(one_play.PLAYER1_ID)
                            on_court_away_player_id.append(one_play.PLAYER2_ID)
                        else:
                            on_court_home_player_id.remove(one_play.PLAYER1_ID)
                            on_court_home_player_id.append(one_play.PLAYER2_ID)
                    except:
                        pass
            last_elapsed_seconds = elapsed_seconds
            if score_diff != 0:
                last_score = one_play.SCORE
        return self.box_score_data
    
    def _get_elapsed_seconds(self, quarter: int, game_clock: str) -> int:
        quarter_length = 12 * 60 

        minutes, seconds = map(int, game_clock.split(":"))
        remaining_seconds = minutes * 60 + seconds

        elapsed_seconds = (quarter - 1) * quarter_length + (quarter_length - remaining_seconds)
        return elapsed_seconds
    
    def _calc_score_diff(self, score1: str, score2: str) -> int:
        if score1 == None or score2 == None:
            return 0
        def extract_away_home(score: str) -> tuple[int, int]:
            match = re.match(r"(\d{1,3})\s*-\s*(\d{1,3})", score)
            if not match:
                raise ValueError(f"Invalid score format: {score}")
            away, home = match.groups()
            return int(away), int(home)

        away1, home1 = extract_away_home(score1)
        away2, home2 = extract_away_home(score2)

        return abs((away2 + home2) - (away1 + home1))
    
    def _append_box_score(self, player_id: int, elapsed_seconds: int ,increments: dict):
        player_last_data = self.box_score_data.data[player_id][-1][1] if self.box_score_data.data[player_id] else [0] * len(vars(ALLOWED_KEYS))
        self.box_score_data.data[player_id].append((
            elapsed_seconds, 
            [v + increments.get(i, 0) for i, v in enumerate(player_last_data)]
        ))
        return
    
    def _contains_3pt(self, str1: str | None, str2: str | None) -> bool:
        if str1 is None and str2 is None:
            return False
        return ' 3PT ' in (str1 or '') or ' 3PT ' in (str2 or '')

    def _extract_off_def(self, str1: str | None, str2: str | None) -> dict:
        if str1 is None and str2 is None:
            return {"off": 0, "def": 0}
        combined = (str1 or '') + ' ' + (str2 or '')
        match = re.search(r'\(Off:(\d+)\s+Def:(\d+)\)', combined)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            return {"off": x, "def": y}
        return {"off": 0, "def": 0}
