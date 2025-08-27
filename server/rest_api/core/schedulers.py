from apscheduler.schedulers.background import BackgroundScheduler

from rest_api.jobs.box_score import daily_box_score_job
from rest_api.jobs.game_summaries import initialize_game_summaries, daily_game_summary_job
from rest_api.jobs.season_summaries import initialize_season_summaries, daily_season_summary_job

scheduler = BackgroundScheduler()

def start_scheduler():
    print(f"[Scheduler] Starting scheduler.")
    scheduler.start()
    initialize_game_summaries(scheduler)
    initialize_season_summaries(scheduler)
    daily_box_score_job(scheduler)
    daily_game_summary_job(scheduler)
    daily_season_summary_job(scheduler)

