from apscheduler.schedulers.background import BackgroundScheduler

from rest_api.jobs.box_score import daily_box_score_job
from rest_api.jobs.game_summaries import (
    daily_game_summary_job,
    initialize_game_summaries,
)
from rest_api.jobs.live_games import update_live_games_job
from rest_api.jobs.season_summaries import (
    daily_season_summary_job,
    initialize_season_summaries,
)

scheduler = BackgroundScheduler()


def start_scheduler():
    print("[Scheduler] Starting scheduler.")
    scheduler.start()
    initialize_game_summaries(scheduler)
    initialize_season_summaries(scheduler)
    daily_box_score_job(scheduler)
    daily_game_summary_job(scheduler)
    daily_season_summary_job(scheduler)
    update_live_games_job(scheduler)
