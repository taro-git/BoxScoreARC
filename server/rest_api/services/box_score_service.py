
import copy
import re
from pandas import DataFrame
from typing import List

from django.db import transaction, IntegrityError
from nba_api.stats.endpoints import playbyplayv2, boxscoretraditionalv3

from rest_api.models.box_score import BoxScore
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus
from rest_api.serializers.box_score import BoxScoreSerializer, BoxScoreCreate, PlayerOnBoxScoreCreate
from rest_api.utils.fetch_player_on_game import fetch_player_on_game, PlayersDict

##
## Fetch from nba_api
#### 
class BoxScoreCreateMaker():
    def __init__(self, game_id: str, final_seconds: int, home_players: List[PlayerOnBoxScoreCreate], away_players: List[PlayerOnBoxScoreCreate]):
        self.game_id: str = game_id
        self.final_seconds: int = final_seconds
        self.home_players: List[PlayerOnBoxScoreCreate] = home_players
        self.away_players: List[PlayerOnBoxScoreCreate] = away_players
    
    def home_player_ids(self) -> List[int]:
        """ホームプレイヤーの player_id 一覧を返します"""
        return [player['player_id'] for player in self.home_players]
    
    def init_player(self, elapsed_seconds: int, player_id: int, is_home_player: bool) -> None:
        """初めてコートインするプレイヤーをボックススコアに追加します."""
        if player_id not in [player['player_id'] for player in self.home_players + self.away_players]:
            init_player_data = PlayerOnBoxScoreCreate({
                'player_id': player_id,
                'box_score_data': [{
                    'elapsed_seconds': elapsed_seconds,
                    'is_on_court': True,
                    'sec': 0,
                    'pts': 0,
                    'reb': 0,
                    'ast': 0,
                    'stl': 0,
                    'blk': 0,
                    'fg': 0,
                    'fga': 0,
                    'three': 0,
                    'threea': 0,
                    'ft': 0,
                    'fta': 0,
                    'oreb': 0,
                    'dreb': 0,
                    'to': 0,
                    'pf': 0,
                    'plusminus': 0,
                }]
            })
            if is_home_player:
                self.home_players.append(init_player_data)
            else:
                self.away_players.append(init_player_data)
    
    def append_box_score_data(self, elapsed_seconds: int, player_id: int, is_home_player: bool, keys: List[str], add_values: List[int]) -> None:
        """ボックススコアにデータを追加します.  
        keys と add_values のインデックスはそろえてください."""
        self.init_player(elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player['player_id'] == player_id:
                new_data = copy.deepcopy(player['box_score_data'][-1])
                new_data['elapsed_seconds'] = elapsed_seconds
                for i, key in enumerate(keys):
                    new_data[key] += add_values[i]
                player['box_score_data'].append(new_data)
    
    def players_to_bench(self, last_elapsed_seconds: int, elapsed_seconds: int, player_ids: List[int], is_home_player: bool) -> None:
        """player_ids で指定した選手一覧をベンチに移動させます.  
        プレイヤーの初期追加が未実施の場合は実施します."""
        for player_id in player_ids:
            self.init_player(last_elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player['player_id'] in player_ids:
                data = player['box_score_data']
                data.append(data[-1])
                data[-1]['elapsed_seconds'] = elapsed_seconds
                data[-1]['is_on_court'] = False
    
    def players_to_court(self, last_elapsed_seconds: int, elapsed_seconds: int, player_ids: List[int], is_home_player: bool) -> None:
        """player_ids で指定した選手一覧をコートに移動させます.  
        プレイヤーの初期追加が未実施の場合は実施します."""
        for player_id in player_ids:
            self.init_player(last_elapsed_seconds, player_id, is_home_player)
        players = self.home_players if is_home_player else self.away_players
        for player in players:
            if player['player_id'] in player_ids:
                data = player['box_score_data']
                data = player['box_score_data']
                data.append(data[-1])
                data[-1]['elapsed_seconds'] = last_elapsed_seconds
                data[-1]['is_on_court'] = True
                data.append(data[-1])
                data[-1]['elapsed_seconds'] = elapsed_seconds
                data[-1]['is_on_court'] = True
    
    def to_box_score_create(self) -> BoxScoreCreate:
        """BoxScoreCreate クラスを生成します."""
        return BoxScoreCreate({
            'game_id': self.game_id,
            'final_seconds': self.final_seconds,
            'home_players': self.home_players,
            'away_players': self.away_players
        })


def fetch_box_score(game_id: str, box_score_status: ScheduledBoxScoreStatus) -> BoxScoreCreate:
    """指定の game_id の PlayByPlay を nba_api から取得し、BoxScoreCreate クラスを生成します."""
    play_by_play_v2 = playbyplayv2.PlayByPlayV2(game_id=game_id)
    box_score_status.progress = 7
    box_score_status.save()
    play_by_play = play_by_play_v2.play_by_play.get_data_frame()
    players = fetch_player_on_game(game_id)
    box_score_status.progress = 24
    box_score_status.save()
    return _convert_play_by_play_to_box_score_create(game_id, play_by_play, players, box_score_status)


def _convert_play_by_play_to_box_score_create(
        game_id: str,
        play_by_play: DataFrame,
        players_info: PlayersDict,
        box_score_status: ScheduledBoxScoreStatus
    ) -> BoxScoreCreate:
    on_court_home_player_ids = [players_info['home_players'][i]['player_id'] for i in range(5)]
    on_court_away_player_ids = [players_info['away_players'][i]['player_id'] for i in range(5)]
    last_score = '0 - 0'
    last_elapsed_seconds = 0
    box_score_create_maker = BoxScoreCreateMaker(game_id, 0, [], [])
    # スターターをボックススコアに登録
    for home_player_id in on_court_home_player_ids:
        box_score_create_maker.init_player(0, home_player_id, True)
    for away_player_id in on_court_away_player_ids:
        box_score_create_maker.init_player(0, away_player_id, False)
    length_of_play_by_play = len(play_by_play)
    change_period_flag = False
    for i, one_play in enumerate(play_by_play.itertuples()):
        progressing = 24 + round((i + 1)/length_of_play_by_play*75)
        if box_score_status.progress + 4 < progressing:
            box_score_status.progress = progressing
            box_score_status.save()
        elapsed_seconds = _get_elapsed_seconds(one_play.PERIOD, one_play.PCTIMESTRING)
        elapsed_seconds_diff = elapsed_seconds - last_elapsed_seconds
        # ピリオド間の選手交代
        if change_period_flag and elapsed_seconds_diff != 0:
            # 交代後に出場する選手の player_id を取得
            on_court_player_ids = _update_on_court_player_id(
                game_id=game_id,
                on_court_home_player_id=on_court_home_player_ids,
                on_court_away_player_id=on_court_away_player_ids,
                home_team_id=players_info['home_team_id'],
                away_team_id=players_info['away_team_id'],
                elapsed_seconds_untill_first_play=elapsed_seconds_diff,
                period=one_play.PERIOD
            )
            # box_score_create に交代を反映
            to_bench_home = list(set(on_court_home_player_ids) - set(on_court_player_ids['home']))
            box_score_create_maker.players_to_bench(last_elapsed_seconds, elapsed_seconds, to_bench_home, True)
            to_bench_away = list(set(on_court_away_player_ids) - set(on_court_player_ids['away']))
            box_score_create_maker.players_to_bench(last_elapsed_seconds, elapsed_seconds, to_bench_away, False)
            to_court_home = list(set(on_court_player_ids['home']) - set(on_court_home_player_ids))
            box_score_create_maker.players_to_court(last_elapsed_seconds, elapsed_seconds, to_court_home, True)
            to_court_away = list(set(on_court_player_ids['away']) - set(on_court_away_player_ids))
            box_score_create_maker.players_to_court(last_elapsed_seconds, elapsed_seconds, to_court_away, False)
            # 交代処理が完了したので、データの更新
            on_court_home_player_ids = on_court_player_ids['home']
            on_court_away_player_ids = on_court_player_ids['away']
            change_period_flag = False
        # 出場中の選手の出場時間を加算
        # nba_api （裏のAPI側）のバグでオンコートプレイヤーが不正確なため、不正確
        for on_court_home_player_id in on_court_home_player_ids:
            box_score_create_maker.append_box_score_data(
                elapsed_seconds,
                on_court_home_player_id,
                True,
                ['sec'],
                [elapsed_seconds_diff]
            )
        for on_court_away_player_id in on_court_away_player_ids:
            box_score_create_maker.append_box_score_data(
                elapsed_seconds,
                on_court_away_player_id,
                False,
                ['sec'],
                [elapsed_seconds_diff]
            )
        # 1プレイを分類し、関連する選手のボックススコアを更新
        score_diff = _calc_score_diff(one_play.SCORE, last_score)
        is_home_player = one_play.PLAYER1_ID in box_score_create_maker.home_player_ids()
        match one_play.EVENTMSGTYPE:
            # フィールドゴール成功
            case 1:
                box_score_create_maker.append_box_score_data(
                    elapsed_seconds,
                    one_play.PLAYER1_ID,
                    is_home_player,
                    ['pts', 'fg', 'fga', 'three', 'threea'],
                    [score_diff, 1, 1, score_diff-2, score_diff-2]
                )
                if one_play.PLAYER2_ID != 0:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        one_play.PLAYER2_ID,
                        is_home_player,
                        ['ast'],
                        [1]
                    )
                # nba_api （裏のAPI側）のバグでオンコートプレイヤーが不正確のため、不正確
                for on_court_home_player_id in on_court_home_player_ids:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        on_court_home_player_id,
                        is_home_player,
                        ['plusminus'],
                        [score_diff if is_home_player else -score_diff],
                    )
                for on_court_away_player_id in on_court_away_player_ids:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        on_court_away_player_id,
                        not is_home_player,
                        ['plusminus'],
                        [-score_diff if is_home_player else score_diff],
                    )
            # フィールドゴール失敗
            case 2:
                box_score_create_maker.append_box_score_data(
                    elapsed_seconds,
                    one_play.PLAYER1_ID,
                    is_home_player,
                    ['fga', 'threea'],
                    [1, 1 if _contains_3pt(one_play.HOMEDESCRIPTION, one_play.VISITORDESCRIPTION) else 0]
                )
                if one_play.PLAYER3_ID != 0:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        one_play.PLAYER3_ID,
                        not is_home_player,
                        ['blk'],
                        [1]
                    )
            # フリースロー試投
            case 3:
                box_score_create_maker.append_box_score_data(
                    elapsed_seconds,
                    one_play.PLAYER1_ID,
                    is_home_player,
                    ['pts', 'ft', 'fta'],
                    [score_diff, score_diff, 1]
                )
                # nba_api （裏のAPI側）のバグでオンコートプレイヤーが不正確なため、不正確
                for on_court_home_player_id in on_court_home_player_ids:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        on_court_home_player_id,
                        is_home_player,
                        ['plusminus'],
                        [score_diff if is_home_player else -score_diff],
                    )
                for on_court_away_player_id in on_court_away_player_ids:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        on_court_away_player_id,
                        not is_home_player,
                        ['plusminus'],
                        [-score_diff if is_home_player else score_diff],
                    )
            # リバウンド獲得
            case 4:
                comulative_reb = _extract_off_def(one_play.HOMEDESCRIPTION, one_play.VISITORDESCRIPTION)
                players = box_score_create_maker.home_players if is_home_player else box_score_create_maker.away_players
                for player in players:
                    if player['player_id'] == one_play.PLAYER1_ID:
                        last_dreb = player['box_score_data'][-1]['dreb']
                        last_oreb = player['box_score_data'][-1]['oreb']
                        box_score_create_maker.append_box_score_data(
                            elapsed_seconds,
                            one_play.PLAYER1_ID,
                            is_home_player,
                            ['reb', 'dreb', 'oreb'],
                            [1, comulative_reb['def'] - last_dreb, comulative_reb['off'] - last_oreb]
                        )
            # ターンオーバー
            case 5:
                box_score_create_maker.append_box_score_data(
                    elapsed_seconds,
                    one_play.PLAYER1_ID,
                    is_home_player,
                    ['to'],
                    [1]
                )
                if one_play.PLAYER2_ID != 0:
                    box_score_create_maker.append_box_score_data(
                        elapsed_seconds,
                        one_play.PLAYER2_ID,
                        not is_home_player,
                        ['stl'],
                        [1]
                    )
            # ファウル
            case 6:
                box_score_create_maker.append_box_score_data(
                    elapsed_seconds,
                    one_play.PLAYER1_ID,
                    is_home_player,
                    ['pf'],
                    [1]
                )
            # ターンオーバーを伴わないバイオレーション
            case 7:
                pass
            # 選手交代
            case 8:
                box_score_create_maker.players_to_bench(last_elapsed_seconds, elapsed_seconds, [one_play.PLAYER1_ID], is_home_player)
                box_score_create_maker.players_to_court(last_elapsed_seconds, elapsed_seconds, [one_play.PLAYER2_ID], is_home_player)
                if is_home_player:
                    if one_play.PLAYER1_ID in on_court_home_player_ids:
                        on_court_home_player_ids.remove(one_play.PLAYER1_ID)
                    on_court_home_player_ids.append(one_play.PLAYER2_ID)
                else:
                    if one_play.PLAYER1_ID in on_court_away_player_ids:
                        on_court_away_player_ids.remove(one_play.PLAYER1_ID)
                    on_court_away_player_ids.append(one_play.PLAYER2_ID)
            # タイムアウト
            case 9:
                pass
            # ティップオフ
            case 10:
                pass
            # 退場
            case 11:
                pass
            # ピリオドの開始
            case 12:
                pass
            # ピリオドの終了
            case 13:
                change_period_flag = True
            # チャレンジによるインスタントリプレイ
            case 18:
                pass
        last_elapsed_seconds = elapsed_seconds
        if score_diff != 0:
            last_score = one_play.SCORE
    box_score_create_maker.final_seconds = last_elapsed_seconds
    return box_score_create_maker.to_box_score_create()


def _get_elapsed_seconds(quarter: int, game_clock: str) -> int:
    """ゲームクロックの文字列から試合経過時間 (秒) を返します."""
    quarter_length = 12 * 60 
    over_time_length = 5 * 60

    minutes, seconds = map(int, game_clock.split(":"))
    remaining_seconds = minutes * 60 + seconds

    if quarter <= 4:
        elapsed_seconds = (quarter - 1) * quarter_length + (quarter_length - remaining_seconds)
    else:
        elapsed_seconds = 4 * 12 * 60 + (quarter - 5) * over_time_length + (over_time_length - remaining_seconds)
    return elapsed_seconds


def _calc_score_diff(score1: str, score2: str) -> int:
    """スコアの文字列から得点差を返します."""
    if score1 == None or score2 == None:
        return 0
    def _extract_away_home(score: str) -> tuple[int, int]:
        match = re.match(r"(\d{1,3})\s*-\s*(\d{1,3})", score)
        if not match:
            raise ValueError(f"Invalid score format: {score}")
        away, home = match.groups()
        return int(away), int(home)

    away1, home1 = _extract_away_home(score1)
    away2, home2 = _extract_away_home(score2)

    return abs((away2 + home2) - (away1 + home1))


def _contains_3pt(str1: str | None, str2: str | None) -> bool:
    """外したシュートが3ptかどうか判定します."""
    if str1 is None and str2 is None:
        return False
    return ' 3PT ' in (str1 or '') or ' 3PT ' in (str2 or '')


def _extract_off_def(str1: str | None, str2: str | None) -> dict:
    """リバウンドを獲得し、オフェンスリバウンドとディフェンスリバウンドの各累計を返します."""
    if str1 is None and str2 is None:
        return {"off": 0, "def": 0}
    combined = (str1 or '') + ' ' + (str2 or '')
    match = re.search(r'\(Off:(\d+)\s+Def:(\d+)\)', combined)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        return {"off": x, "def": y}
    return {"off": 0, "def": 0}


def _update_on_court_player_id(
        game_id: str,
        on_court_home_player_id: List[int],
        on_court_away_player_id: List[int],
        home_team_id: int,
        away_team_id: int,
        elapsed_seconds_untill_first_play: int,
        period: int,
    ) -> dict:
    """ピリオド間の選手交代を検知し、出場選手を返します.  
    note: boxscoretraditionalv3 側にバグがあり、空の配列を返してしまっています."""
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
    try:
        player_stats = box_score_traditional_v3.player_stats.get_data_frame()
    except Exception as e:
        # 稀に boxscoretraditionalv3 のレスポンスデータが不正でget_data_frame() できないことがある 
        # nba_api 自体か裏で叩いている nba 側の API でのバグのため、暫定で以下の処理で対応
        print("get_data_frame() でエラー:", e)

        headers = box_score_traditional_v3.player_stats.data["headers"]
        data = box_score_traditional_v3.player_stats.data["data"]

        expected_col_count = len(headers)
        trimmed_data = []

        for row in data:
            row = list(row)

            diff = len(row) - expected_col_count
            if diff <= 0:
                # 行が短いか期待列数と同じならそのまま
                trimmed_data.append(row)
                continue

            # 差分分だけ None を削除（左から順に）
            none_indices = [i for i, v in enumerate(row) if v is None]
            to_remove = min(diff, len(none_indices))

            # None を左から to_remove 個削除
            for idx in sorted(none_indices[:to_remove], reverse=True):
                del row[idx]

            diff -= to_remove

            # まだ差分が残っていれば、末尾から切り詰める
            if diff > 0:
                row = row[:-diff]

            trimmed_data.append(row)

        # headers はそのまま使う（length = expected_col_count）
        player_stats = DataFrame(trimmed_data, columns=headers)
    home_player_stats = player_stats[
        (player_stats["teamId"] == home_team_id) &
        (player_stats["minutes"].apply(_convert_clock_to_seconds) >= elapsed_seconds_untill_first_play)
    ]
    away_player_stats = player_stats[
        (player_stats["teamId"] == away_team_id) &
        (player_stats["minutes"].apply(_convert_clock_to_seconds) >= elapsed_seconds_untill_first_play)
    ]

    home_player_id = []
    if len(home_player_stats) == 5:
        home_player_id = home_player_stats["personId"].tolist()
    elif len(home_player_stats["minutes"].unique()) == 3:
        home_seconds_with_ended_period = home_player_stats["minutes"].apply(_convert_clock_to_seconds).max()
        home_player_id = home_player_stats[
            (home_player_stats["minutes"].apply(_convert_clock_to_seconds) == elapsed_seconds_untill_first_play) |
            (home_player_stats["minutes"].apply(_convert_clock_to_seconds) == home_seconds_with_ended_period)
        ]["personId"].tolist()
    elif len(home_player_stats["minutes"].unique()) == 1:
        home_player_id = home_player_stats[home_player_stats["personId"].isin(on_court_home_player_id)]["personId"].tolist()
    elif len(home_player_stats["minutes"].unique()) == 2:
        home_seconds_with_ended_period = home_player_stats["minutes"].apply(_convert_clock_to_seconds).max()
        home_player_id = home_player_stats[
            (home_player_stats["minutes"].apply(_convert_clock_to_seconds) == home_seconds_with_ended_period) |
            (home_player_stats["personId"].isin(on_court_home_player_id))
        ]["personId"].tolist()
    away_player_id = []
    if len(away_player_stats) == 5:
        away_player_id = away_player_stats["personId"].tolist()
    elif len(away_player_stats["minutes"].unique()) == 3:
        away_seconds_with_ended_period = away_player_stats["minutes"].apply(_convert_clock_to_seconds).max()
        away_player_id = away_player_stats[
            (away_player_stats["minutes"].apply(_convert_clock_to_seconds) == elapsed_seconds_untill_first_play) |
            (away_player_stats["minutes"].apply(_convert_clock_to_seconds) == away_seconds_with_ended_period)
        ]["personId"].tolist()
    elif len(away_player_stats["minutes"].unique()) == 1:
        away_player_id = away_player_stats[away_player_stats["personId"].isin(on_court_away_player_id)]["personId"].tolist()
    elif len(away_player_stats["minutes"].unique()) == 2:
        away_seconds_with_ended_period = away_player_stats["minutes"].apply(_convert_clock_to_seconds).max()
        away_player_id = away_player_stats[
            (away_player_stats["minutes"].apply(_convert_clock_to_seconds) == away_seconds_with_ended_period) |
            (away_player_stats["personId"].isin(on_court_away_player_id))
        ]["personId"].tolist()

    return { 'home': home_player_id, 'away': away_player_id }


def _convert_clock_to_seconds(clock: str) -> int:
    """ゲームクロックの文字列を秒数に変換します."""
    try:
        minutes, seconds = map(int, clock.split(":"))
    except:
        return 0
    return minutes * 60 + seconds

##
## Upsert to DB
#### 
def upsert_box_score(box_score_create: BoxScoreCreate):
    """指定の game_id の BoxScore が、なければ新規作成、あれば更新します."""

    game_id = box_score_create.get("game_id")
    if not game_id:
        raise ValueError("Game ID is not set")

    try:
        with transaction.atomic():
            instance = BoxScore.objects.filter(game_id=game_id).first()
            serializer = BoxScoreSerializer(instance=instance, data=box_score_create)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
    except IntegrityError as e:
        raise ValueError(f"DB制約違反: {e}")
    except ValueError as ve:
        raise ve 
