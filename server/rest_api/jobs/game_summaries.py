from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.utils.timezone import make_aware

from rest_api.models.game_summary import GameSummary
from rest_api.services.game_summary_service import (
    fetch_game_summaries_by_season,
    get_regular_season_team_ids_by_season,
    upsert_game_summary,
)


def initialize_game_summaries(scheduler: BackgroundScheduler):
    """game summary の初期化をします.
    15分ごとにnba_api をたたいて、game summary を DB にインサートします."""
    print("[scheduler] add initialize_game_summaries")
    scheduler.add_job(
        func=lambda: _initialize_game_summaries(scheduler),
        trigger=IntervalTrigger(minutes=15),
        id="initialize_game_summaries",
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _initialize_game_summaries(scheduler: BackgroundScheduler):
    """今年から来年にかけてのシーズンから、1990-91シーズンまでを準備します.
    1回の実行でDBに存在しないシーズン1つについてfetch, upsert を実行します."""
    years = list(range(datetime.now().year, 1989, -1))
    for year in years:
        season = f"{year}-{(year + 1) % 100:02d}"
        print(f"[scheduler] initializing game summaries, in {season}")
        season_game_exists = len(get_regular_season_team_ids_by_season(season)) > 0
        if not season_game_exists:
            try:
                print(f"[scheduler] try to fetch and upsert game summaries, season is {season}")
                game_summaries = fetch_game_summaries_by_season(season)
                for game_summary in game_summaries:
                    try:
                        upsert_game_summary(game_summary)
                    except Exception:
                        print(
                            f"[scheduler] error in upsert_game_summary, "
                            f"{game_summary.get('home_team_abb', 'unknown')} "
                            f"vs. {game_summary.get('away_team_abb', 'unknown')} "
                            f"at {game_summary.get('game_datetime', 'unknown')}"
                        )
                if len(game_summaries) > 0:
                    print(f"success upsert season {season}")
                    return
            except Exception as e:
                print(f"[scheduler] error in fetch_game_summaries_by_season, {season}. {e}")
    print("[scheduler] remove initialize_game_summaries")
    scheduler.remove_job(job_id="initialize_game_summaries", jobstore=None)
    return


def daily_game_summary_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.
    nba_api をたたいて、当日以降の game summary を挿入・更新します."""
    print("[scheduler] add daily job: game summary")
    scheduler.add_job(
        func=_daily_game_summary_jobs,
        trigger=CronTrigger(hour=0, minute=25),
        id="daily_game_summary_job",
        replace_existing=True,
    )


def _daily_game_summary_jobs():
    """nba_api をたたいて、以下の game summary を挿入・更新します.
    1. 当日以降のもの
    2. 過去実施済みにも関わらず DB 上のステータスが試合終了となっていないもの"""
    print(f"[scheduler] start daily job at {datetime.now()}: game summary")
    invalid_game_summaries = GameSummary.objects.filter(game_datetime__lte=(make_aware(datetime.now()))).exclude(
        status_id=3
    )
    invalid_game_ids = [game_summary.game_id for game_summary in invalid_game_summaries]
    today = datetime.now(ZoneInfo("America/New_York")).replace(hour=0, minute=0, second=0, microsecond=0)
    this_year = today.year
    years = list(range(this_year, this_year - 2, -1))
    for year in years:
        try:
            season = f"{year}-{(year + 1) % 100:02d}"
            print(f"[scheduler] fetch game summaries {season}")
            game_summaries = fetch_game_summaries_by_season(season)
            for game_summary in [
                game_summary
                for game_summary in game_summaries
                if game_summary["game_datetime"] > today
                or (game_summary["game_id"] in invalid_game_ids and game_summary["status_id"] == 3)
            ]:
                try:
                    upsert_game_summary(game_summary)
                except Exception:
                    print(
                        f"[scheduler] error in upsert_game_summary, "
                        f"{game_summary.get('home_team_abb', 'unknown')} "
                        f"vs. {game_summary.get('away_team_abb', 'unknown')} "
                        f"at {game_summary.get('game_datetime', 'unknown')}"
                    )
            print(f"[scheduler] upsert game summaries {season}")
        except Exception as e:
            print(f"[scheduler] error in fetch in {season}. {e}")
    print(f"[scheduler] finish daily job at {datetime.now()}: game summary")
    return
