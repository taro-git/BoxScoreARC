from datetime import datetime

from django.utils.timezone import make_aware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from rest_api.models.game_summary import GameSummary
from rest_api.services.game_summary_service import fetch_game_summaries_by_season, upsert_game_summary

scheduler = BackgroundScheduler()


def initialize_game_summaries(scheduler: BackgroundScheduler):
    """game summary の初期化をします.  
    15分ごとにnba_api をたたいて、game summary を DB にインサートします."""
    scheduler.add_job(
        func=_initialize_game_summaries,
        trigger=IntervalTrigger(minutes=15),
        id='initialize_game_summaries',
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _initialize_game_summaries():
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
                    upsert_game_summary(game_summary)
                if len(game_summaries) > 0:
                    print(f'success upsert season {season}')
                    print(datetime.now())
                    return
            except Exception as e:
                print(f'[scheduler] error in fetch or upsert in {season}. {e}')
    print('[scheduler] remove initialize_game_summaries')
    scheduler.remove_executor('initialize_game_summaries')
    return
    


