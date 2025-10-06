from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from rest_api.models.box_score import BoxScore
from rest_api.models.game_summary import GameSummary
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus


def daily_box_score_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.
    正しいデータではないbox score を削除します."""
    print("[scheduler] add daily job: box score")
    scheduler.add_job(
        func=_daily_box_score_jobs,
        trigger=CronTrigger(hour=0, minute=0),
        id="daily_box_score_job",
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _daily_box_score_jobs():
    print(f"[scheduler] start daily job at {datetime.now()}: box score")
    box_scores = BoxScore.objects.all()
    game_summaries = GameSummary.objects.filter(game_id__in=[bs.game_id.game_id for bs in box_scores])
    invalid_game_summary_ids = [
        gs for gs in game_summaries if len(gs.home_players_on_game) < 8 or len(gs.away_players_on_game) < 8
    ]
    box_scores = [bs for bs in box_scores if not bs.is_collect or bs.game_id.game_id in invalid_game_summary_ids]
    for box_score in box_scores:
        ScheduledBoxScoreStatus.objects.filter(game_id=box_score.game_id.game_id).delete()
        box_score.delete()
    ScheduledBoxScoreStatus.objects.filter(error_message__isnull=False).delete()
    print(f"[scheduler] finish daily job at {datetime.now()}: box score")
