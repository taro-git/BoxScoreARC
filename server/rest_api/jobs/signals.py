import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus
from rest_api.services.box_score_service import fetch_box_score, upsert_box_score
from rest_api.services.game_summary_service import (
    update_players_in_game_summary_by_game_id,
    upsert_game_summary,
)


def _make_box_score_data(instance: ScheduledBoxScoreStatus):
    """nba_api を利用して、ボックススコアのデータを作成し、DB に保存します."""
    try:
        instance.progress = 1
        instance.save()
        game_summary_create = update_players_in_game_summary_by_game_id(instance.game_id.game_id)
        instance.progress = 30
        instance.save()
        box_score_create = fetch_box_score(instance.game_id.game_id, instance)
        home_score = sum([p["box_score_data"][-1]["pts"] for p in box_score_create["home_players"]])
        away_score = sum([p["box_score_data"][-1]["pts"] for p in box_score_create["away_players"]])
        if home_score == game_summary_create["home_score"] and away_score == game_summary_create["away_score"]:
            upsert_game_summary(game_summary_create)
            upsert_box_score(box_score_create)
            instance.progress = 100
            instance.save()
        else:
            print(
                f"score is not match."
                f" from game summary: {game_summary_create['away_score']} - {game_summary_create['home_score']}"
                f" from box score: {away_score} - {home_score}"
            )
            instance.delete()
            print(f"delete scheduled box score status record; game id is {game_summary_create['game_id']}")
    except Exception as e:
        instance.error_message = str(e)
        instance.save()


@receiver(post_save, sender=ScheduledBoxScoreStatus)
def handle_status_update(sender, instance, **kwargs):
    """status が progressing のものが存在せず、status が pending のものが存在するとき、
    pending のうち登録日時が最古のgameについて、DBに BoxScore をupsert します."""
    if (
        ScheduledBoxScoreStatus.objects.filter(progress=0, error_message__isnull=True).exists()
        and not ScheduledBoxScoreStatus.objects.filter(
            progress__gt=0, progress__lt=100, error_message__isnull=True
        ).exists()
    ):
        oldest_pending = (
            ScheduledBoxScoreStatus.objects.filter(progress=0, error_message__isnull=True)
            .order_by("registered_datetime")
            .first()
        )
        threading.Thread(target=_make_box_score_data, args=(oldest_pending,), daemon=True).start()
