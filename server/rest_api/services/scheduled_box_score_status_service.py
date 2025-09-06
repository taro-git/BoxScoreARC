from django.db import transaction, IntegrityError

from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus
from rest_api.serializers.scheduled_box_score_status import ScheduledBoxScoreStatusCreate, ScheduledBoxScoreStatusSerializer

##
## Upsert to DB
#### 
def upsert_scheduled_box_score_status(scheduled_box_score_status_create: ScheduledBoxScoreStatusCreate):
    """指定の scheduled box score status が、なければ新規作成、あれば更新します."""

    game_id = scheduled_box_score_status_create.get("game_id")
    if not game_id:
        raise ValueError("game id is not set")

    try:
        with transaction.atomic():
            instance = ScheduledBoxScoreStatus.objects.filter(game_id=game_id).first()
            serializer = ScheduledBoxScoreStatusSerializer(instance=instance, data=scheduled_box_score_status_create)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
    except IntegrityError as e:
        raise ValueError(f"DB制約違反: {e}")
    except ValueError as ve:
        raise ve 