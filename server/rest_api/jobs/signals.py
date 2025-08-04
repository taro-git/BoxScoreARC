import threading
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus

from rest_api.services.box_score_service import fetch_box_score, upsert_box_score

def _make_box_score_data(instance: ScheduledBoxScoreStatus):
    """nba_api を利用して、ボックススコアのデータを作成し、DB に保存します."""
    try:
        instance.progress = 1
        instance.save()
        box_score_create = fetch_box_score(instance.game_id.game_id, instance)
        upsert_box_score(box_score_create)
        instance.progress = 100
        instance.save()
    except Exception as e:
        instance.error_message = e
        instance.save()


@receiver(post_save, sender=ScheduledBoxScoreStatus)
def handle_status_update(sender, instance, **kwargs):
    """status が progressing のものが存在せず、status が pending のものが存在するとき、  
    pending のうち登録日時が最古のgameについて、DBに BoxScore をupsert します."""
    if (
        ScheduledBoxScoreStatus.objects.filter(progress=0, error_message__isnull=True).exists() and
        not ScheduledBoxScoreStatus.objects.filter(progress__gt=0, progress__lt=100, error_message__isnull=True).exists()
    ):
        oldest_pending = ScheduledBoxScoreStatus.objects.filter(
            progress=0, error_message__isnull=True
        ).order_by('registered_datetime').first()
        threading.Thread(target=_make_box_score_data, args=(oldest_pending,), daemon=True).start()
