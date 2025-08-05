from datetime import datetime
from zoneinfo import ZoneInfo

from django.utils.timezone import make_aware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from rest_api.models.game_summary import GameSummary
from rest_api.services.game_summary_service import fetch_game_summaries_by_season, upsert_game_summary


def initialize_game_summaries(scheduler: BackgroundScheduler):
    """game summary の初期化をします.  
    15分ごとにnba_api をたたいて、game summary を DB にインサートします."""
    scheduler.add_job(
        func=lambda: _initialize_game_summaries(scheduler),
        trigger=IntervalTrigger(minutes=15),
        id='initialize_game_summaries',
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _initialize_game_summaries(scheduler: BackgroundScheduler):
    """今年から来年にかけてのシーズンから、1990-91シーズンまでを準備します.  
    1回の実行でDBに存在しないシーズン1つについてfetch, upsert を実行します."""
    years = list(range(datetime.now().year, 1989, -1))
    for year in years:
        season_start = make_aware(datetime(year, 10, 1))
        season_end = make_aware(datetime(year+1, 9, 30, 23, 59, 59))
        season_games = GameSummary.objects.filter(game_datetime__range=(season_start, season_end))
        if not season_games.exists():
            try:
                season = f"{year}-{(year + 1) % 100:02d}"
                game_summaries = fetch_game_summaries_by_season(season)
                for game_summary in game_summaries:
                    try:
                        upsert_game_summary(game_summary)
                    except Exception as e:
                        print(f'[scheduler] error in upsert_game_summary, game id is {game_summary["game_id"]}')
                if len(game_summaries) > 0:
                    print(f'success upsert season {season}')
                    print(datetime.now())
                    return
            except Exception as e:
                print(f'[scheduler] error in fetch in {season}. {e}')
    print('[scheduler] remove initialize_game_summaries')
    scheduler.remove_job('initialize_game_summaries')
    return
    

def daily_game_summary_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.  
    1. nba_api をたたいて、当日以降の game summary を挿入・更新します.  
    2. 当日予定している試合の game summary を20分ごとに更新します.  """
    print('[scheduler] start daily job: game summary')
    scheduler.add_job(
        func=lambda: _daily_game_summary_jobs(scheduler),
        trigger=CronTrigger(hour=0, minute=0),
        id='daily_game_summary_job',
        replace_existing=True,
    )


def _daily_game_summary_jobs(scheduler: BackgroundScheduler):
    _upsert_future_game_summary()
    _make_scheduler_to_update_live_game_summary(scheduler)


def _upsert_future_game_summary():
    """nba_api をたたいて、当日以降の game summary を挿入・更新します.  """
    today = datetime.now(ZoneInfo("America/New_York")).replace(hour=0, minute=0, second=0, microsecond=0)
    this_year = today.year
    years = list(range(this_year, this_year - 2, -1))
    for year in years:
        try:
            season = f"{year}-{(year + 1) % 100:02d}"
            print(f'[scheduler] fetch game summaries {season}')
            game_summaries = fetch_game_summaries_by_season(season)
            for game_summary in [game_summary for game_summary in game_summaries if game_summary['game_datetime'] > today]:
                try:
                    print(f'[scheduler] upsert game summary {game_summary}')
                    upsert_game_summary(game_summary)
                except Exception as e:
                    print(f'[scheduler] error in upsert_game_summary, game id is {game_summary["game_id"]}')
        except Exception as e:
            print(f'[scheduler] error in fetch in {season}. {e}')
    return


def _make_scheduler_to_update_live_game_summary(scheduler: BackgroundScheduler):
    # MYTODO: #34 データベースから当日の試合を検索、試合が無ければ何もしない、あれば game_datetime が一番早いものをnext_run_time に入れる
    # scheduler.add_job(
    #     func=lambda: _update_live_game_summary(scheduler),
    #     trigger=IntervalTrigger(minutes=20),
    #     id='update_live_game_summary',
    #     next_run_time=datetime.now(),
    #     replace_existing=True,
    # )
    return


def _update_live_game_summary(scheduler: BackgroundScheduler):
    # MYTODO: #34 db から日付指定でgamesummary を取得、status id が全部3だったら何もせずにscheduler を削除
    # 1か2の試合が存在していれば、fetch_game_summaries_by_date, update_players_in_game_summary_by_game_id, upsert_game_summary
    return
