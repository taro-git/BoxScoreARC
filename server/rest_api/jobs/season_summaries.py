import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.utils.timezone import make_aware

from rest_api.models.game_summary import GameSummary
from rest_api.models.season_summary import SeasonSummary
from rest_api.services.game_summary_service import get_regular_season_team_ids_by_season
from rest_api.services.season_summary_service import (
    fetch_regular_season_team_stats,
    upsert_season_summary,
)


def initialize_season_summaries(scheduler: BackgroundScheduler):
    """season summary の初期化をします.
    8 時間ごとにnba_api をたたいて、season summary を DB にインサートします."""
    while scheduler.get_job("initialize_game_summaries") is not None:
        print("[scheduler] waiting to finish initializing game summary for initializing season summary")
        time.sleep(60)
    print("[scheduler] add initialize_season_summaries")
    scheduler.add_job(
        func=lambda: _initialize_season_summaries(scheduler),
        trigger=IntervalTrigger(hours=8),
        id="initialize_season_summaries",
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _initialize_season_summaries(scheduler: BackgroundScheduler):
    """今年から来年にかけてのシーズンから、1990-91シーズンまでを準備します.
    1回の実行でDBに存在しないシーズン1つについてfetch, upsert を実行します."""
    years = list(range(datetime.now().year, 1989, -1))
    for year in years:
        season = f"{year}-{(year + 1) % 100:02d}"
        print(f"[scheduler] initialize season summary, season is {season}")
        season_summary = SeasonSummary.objects.filter(season=season)
        if not season_summary.exists():
            _fetch_and_upsert_season_summary(season)
    print("[scheduler] remove initialize_season_summaries")
    scheduler.remove_job("initialize_season_summaries")
    return


def _fetch_and_upsert_season_summary(season: str):
    team_ids = get_regular_season_team_ids_by_season(season)
    teams = []
    for team_id in team_ids:
        try:
            teams.append(fetch_regular_season_team_stats(season, team_id))
            print(f"[scheduler] success fetch_regular_season_team_stats, season is {season}, team_id is {team_id}")
            time.sleep(7 * 60)
        except Exception:
            print(f"[scheduler] error in fetch_regular_season_team_stats, season is {season}, team_id is {team_id}")
            break
    try:
        if len(teams) > 0:
            upsert_season_summary({"season": season, "teams": teams})
            print(f"[scheduler] upsert season summary, season is {season}")
            return
        else:
            print(f"[scheduler] no data about team stats in the season: {season}")
    except Exception:
        print(f"[scheduler] error in upsert_season_summary, season is {season}")
    return


def daily_season_summary_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.
    nba_api をたたいて、前日の試合結果を season summary に反映させます."""
    print("[scheduler] add daily job: season summary")
    scheduler.add_job(
        func=_daily_season_summary_job,
        trigger=CronTrigger(hour=0, minute=0),
        id="daily_season_summary_job",
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _daily_season_summary_job():
    """nba_api をたたいて、前日の試合結果を踏まえた season summary を upsert します."""
    print(f"[scheduler] start daily job at {datetime.now()}: season summary")
    today = datetime.now()
    game_summaries = GameSummary.objects.filter(
        game_datetime__range=(make_aware(today - timedelta(days=1)), make_aware(today)),
        status_id=3,
    )
    seasons = set(
        [game_summary.season for game_summary in game_summaries if game_summary.game_category == "Regular Season"]
    )
    for season in seasons:
        _fetch_and_upsert_season_summary(season)
    print(f"[scheduler] finish daily job at {datetime.now()}: season summary")
