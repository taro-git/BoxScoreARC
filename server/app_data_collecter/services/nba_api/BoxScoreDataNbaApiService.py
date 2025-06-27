import re
import pandas as pd
from types import SimpleNamespace
from nba_api.stats.endpoints import playbyplayv2, boxscoretraditionalv3

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
        # MYTODO min と +/- が正しくない⇒クウォーター間の交代が playbyplay に反映されないことが原因。boxscoretraditionalv3 の end_range, start_rangeで対応可能　スタメンもこれで対応した方がよさげ
        box_score_summary = BoxScoreSummaryNbaApiService().get_box_score_summary(game_id)
        on_court_away_player_id = [box_score_summary.away.players[i].player_id for i in range(5)]
        on_court_home_player_id = [box_score_summary.home.players[i].player_id for i in range(5)]
        change_period_flag = False
        for one_play in play_by_play.itertuples():
            elapsed_seconds = self._get_elapsed_seconds(one_play.PERIOD, one_play.PCTIMESTRING)
            elapsed_seconds_diff = elapsed_seconds - last_elapsed_seconds
            if change_period_flag and elapsed_seconds_diff != 0:
                on_court_player_id = self._update_on_court_player_id(
                    game_id=game_id,
                    on_court_away_player_id=on_court_away_player_id,
                    on_court_home_player_id=on_court_home_player_id,
                    away_team_id=box_score_summary.away.team_id,
                    home_team_id=box_score_summary.home.team_id,
                    elapsed_seconds_untill_first_play=elapsed_seconds_diff,
                    period=one_play.PERIOD
                )
                on_court_away_player_id = on_court_player_id['away']
                on_court_home_player_id = on_court_player_id['home']
                change_period_flag = False
            for player_id in on_court_away_player_id + on_court_home_player_id:
                self._append_box_score(player_id, elapsed_seconds, {
                    ALLOWED_KEYS.MIN: elapsed_seconds_diff
                })
            score_diff = self._calc_score_diff(one_play.SCORE, last_score)
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
                        print("error on_court_player")
                        print(on_court_away_player_id)
                        print(on_court_home_player_id)
                case 12:
                    change_period_flag = True
            last_elapsed_seconds = elapsed_seconds
            if score_diff != 0:
                last_score = one_play.SCORE
        return self.box_score_data
    
    def _get_elapsed_seconds(self, quarter: int, game_clock: str) -> int:
        quarter_length = 12 * 60 
        over_time_length = 5 * 60

        minutes, seconds = map(int, game_clock.split(":"))
        remaining_seconds = minutes * 60 + seconds

        if quarter <= 4:
            elapsed_seconds = (quarter - 1) * quarter_length + (quarter_length - remaining_seconds)
        else:
            elapsed_seconds = 4 * 12 * 60 + (quarter - 5) * over_time_length + (over_time_length - remaining_seconds)
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

    def _convert_clock_to_seconds(self, clock: str) -> int:
        minutes, seconds = map(int, clock.split(":"))
        return minutes * 60 + seconds

    def _update_on_court_player_id(
        self,
        game_id: str,
        on_court_away_player_id: list[int],
        on_court_home_player_id: list[int],
        away_team_id: int,
        home_team_id: int,
        elapsed_seconds_untill_first_play: int,
        period: int,
    ) -> dict:
        pd.set_option('display.max_rows', None)        # 行をすべて表示
        pd.set_option('display.max_columns', None)     # 列をすべて表示
        pd.set_option('display.width', None)           # 横幅による折返しを防止
        pd.set_option('display.max_colwidth', None)    # 各列の内容の最大文字数
        if period <= 4:
            period_start_seconds = 12 * 60 * (period - 1)
        else:
            period_start_seconds = 4 * 12 * 60 + 5 * 60 * (period - 5)
        box_score_traditional_v3 = boxscoretraditionalv3.BoxScoreTraditionalV3(
            game_id=game_id,
            start_period="0",
            start_range=str(period_start_seconds * 10),
            end_period="0",
            end_range=str((period_start_seconds + elapsed_seconds_untill_first_play) * 10),
            range_type="2",
        )
        player_stats = box_score_traditional_v3.player_stats.get_data_frame()
        away_player_stats = player_stats[
            (player_stats["teamId"] == away_team_id) &
            (player_stats["minutes"].apply(self._convert_clock_to_seconds) >= elapsed_seconds_untill_first_play)
        ]
        home_player_stats = player_stats[
            (player_stats["teamId"] == home_team_id) &
            (player_stats["minutes"].apply(self._convert_clock_to_seconds) >= elapsed_seconds_untill_first_play)
        ]
        away_player_id = []
        if len(away_player_stats) == 5:
            away_player_id = away_player_stats["personId"].tolist()
        elif len(away_player_stats["minutes"].unique()) == 3:
            away_seconds_with_ended_period = away_player_stats["minutes"].apply(self._convert_clock_to_seconds).max()
            away_player_id = away_player_stats[
                (away_player_stats["minutes"].apply(self._convert_clock_to_seconds) == elapsed_seconds_untill_first_play) |
                (away_player_stats["minutes"].apply(self._convert_clock_to_seconds) == away_seconds_with_ended_period)
            ]["personId"].tolist()
        elif len(away_player_stats["minutes"].unique()) == 1:
            away_player_id = away_player_stats[away_player_stats["personId"].isin(on_court_away_player_id)]["personId"].tolist()
        elif len(away_player_stats["minutes"].unique()) == 2:
            away_seconds_with_ended_period = away_player_stats["minutes"].apply(self._convert_clock_to_seconds).max()
            away_player_id = away_player_stats[
                (away_player_stats["minutes"].apply(self._convert_clock_to_seconds) == away_seconds_with_ended_period) |
                (away_player_stats["personId"].isin(on_court_away_player_id))
            ]["personId"].tolist()

        home_player_id = []
        if len(home_player_stats) == 5:
            home_player_id = home_player_stats["personId"].tolist()
        elif len(home_player_stats["minutes"].unique()) == 3:
            home_seconds_with_ended_period = home_player_stats["minutes"].apply(self._convert_clock_to_seconds).max()
            home_player_id = home_player_stats[
                (home_player_stats["minutes"].apply(self._convert_clock_to_seconds) == elapsed_seconds_untill_first_play) |
                (home_player_stats["minutes"].apply(self._convert_clock_to_seconds) == home_seconds_with_ended_period)
            ]["personId"].tolist()
        elif len(home_player_stats["minutes"].unique()) == 1:
            home_player_id = home_player_stats[home_player_stats["personId"].isin(on_court_home_player_id)]["personId"].tolist()
        elif len(home_player_stats["minutes"].unique()) == 2:
            home_seconds_with_ended_period = home_player_stats["minutes"].apply(self._convert_clock_to_seconds).max()
            home_player_id = home_player_stats[
                (home_player_stats["minutes"].apply(self._convert_clock_to_seconds) == home_seconds_with_ended_period) |
                (home_player_stats["personId"].isin(on_court_home_player_id))
            ]["personId"].tolist()

        return {'away': away_player_id, 'home': home_player_id}
