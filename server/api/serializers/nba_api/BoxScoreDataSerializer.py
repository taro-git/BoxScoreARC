from rest_framework import serializers
from typing import Dict, List, Tuple

from ...models.nba_api.BoxScoreDataModel import BoxScoreData



class BoxScoreDataSerializer(serializers.Serializer):

    def to_representation(self, instance: BoxScoreData) -> Dict[str, List[List]]:
        result = {}
        for key, entries in instance.data.items():
            result[str(key)] = [[player_id, stats] for player_id, stats in entries]
        return result
