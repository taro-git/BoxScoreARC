from typing import TypedDict

from rest_framework import serializers

from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus


##
## schema for access from django self
####
class ScheduledBoxScoreStatusCreate(TypedDict):
    game_id: str
    error_message: str | None
    progress: int


##
## Serializer
####
class ScheduledBoxScoreStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    registered_datetime = serializers.DateTimeField(write_only=True, required=False, allow_null=True)
    progress = serializers.IntegerField(required=False, allow_null=True, default=0)

    class Meta:
        model = ScheduledBoxScoreStatus
        fields = "__all__"

    def get_status(self, obj):
        return obj.status
