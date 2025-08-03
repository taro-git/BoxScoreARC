import os

from apscheduler.schedulers.background import BackgroundScheduler

from rest_api.models.scheduler_lock import SchedulerLock
from rest_api.jobs.commons import initialize
from rest_api.jobs.game_summaries import initialize_game_summaries

scheduler = BackgroundScheduler()

def start_scheduler():
    try:
        lock_name = f'scheduler-{os.environ["START_EPOCH"]}'
        SchedulerLock.objects.create(name=lock_name)
        print(f"[Scheduler] Lock acquired (PID={os.getpid()}). Starting scheduler.")
        initialize(lock_name)
        scheduler.start()
        initialize_game_summaries(scheduler)
    except Exception as e:
        print(f"[Scheduler] Not started: {e}")
        return
        