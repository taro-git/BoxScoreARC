from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from rest_api.models.box_score import BoxScore
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus


def daily_box_score_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.
    正しいデータではないbox score を削除します."""
    print("[scheduler] add daily job: box score")
    scheduler.add_job(
        func=_daily_box_score_jobs,
        trigger=CronTrigger(hour=0, minute=0),
        id="daily_box_score_job",
        replace_existing=True,
    )


def _daily_box_score_jobs():
    print(f"[scheduler] start daily job at {datetime.now()}: box score")
    box_scores = BoxScore.objects.all()
    box_scores = [box_score for box_score in box_scores if not box_score.is_collect]
    for box_score in box_scores:
        ScheduledBoxScoreStatus.objects.filter(game_id=box_score.game_id.game_id).delete()
    print(f"[scheduler] finish daily job at {datetime.now()}: box score")
