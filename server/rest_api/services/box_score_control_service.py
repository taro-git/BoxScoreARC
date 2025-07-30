from typing import TypedDict, List
from decimal import Decimal

from rest_api.models.box_score import BoxScore
from rest_api.serializers.box_score import BoxScoreSerializer


class BoxScoreDataCreate(TypedDict):
    elapsed_seconds: int
    is_on_court: bool
    min: Decimal
    """整数部最大3桁、小数部2桁"""
    pts: int
    reb: int
    ast: int
    stl: int
    blk: int
    fg: int
    fga: int
    fgper: Decimal
    """整数部最大3桁、小数部2桁"""
    three: int
    threea: int
    threeper: Decimal
    """整数部最大3桁、小数部2桁"""
    ft: int
    fta: int
    ftper: Decimal
    """整数部最大3桁、小数部2桁"""
    oreb: int
    dreb: int
    to: int
    pf: int
    eff: Decimal
    """整数部最大3桁、小数部2桁"""
    plusminus: int

class PlayerOnBoxScoreCreate(TypedDict):
    player_id: int
    box_score_data: List[BoxScoreDataCreate]

class BoxScoreCreate(TypedDict):
    game_id: int
    """GameSummary に存在する game id のみ指定可能"""
    home_players: List[PlayerOnBoxScoreCreate]
    away_players: List[PlayerOnBoxScoreCreate]

def upsert_box_score(box_score_create: BoxScoreCreate):
    """指定の game_id の BoxScore が、なければ新規作成、あれば更新します."""

    game_id = box_score_create.get("game_id")

    if game_id:
        if BoxScore.objects.filter(game_id=game_id).exists():
            instance = BoxScore.objects.get(game_id=game_id)
        else:
            instance = None
        serializer = BoxScoreSerializer(instance=instance, data=box_score_create)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors)
    else:
        raise ValueError('Game ID is not set')

