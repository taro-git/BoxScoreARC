from typing import TypedDict, List
from datetime import datetime
import requests
import base64

from django.core.cache  import cache

from rest_api.models.game_summary import GameSummary, Team
from rest_api.serializers.game_summary import GameSummarySerializer, TeamSerializer


class PlayerOnGameData(TypedDict):
    player_id: int
    name: str
    jersey: str
    position: str
    is_starter: bool
    is_inactive: bool
    sequence: int

class GameSummaryData(TypedDict):
    game_id: int
    sequence: int
    status_id: int
    status_text: str
    live_period: str
    live_clock: str
    game_date_est: datetime
    home_team_id: int
    away_team_id: int
    home_team_abb: str
    away_team_abb: str
    home_score: int
    away_score: int
    home_players: List[PlayerOnGameData]
    away_players: List[PlayerOnGameData]

def upsert_game_summary(game_summary_data: GameSummaryData):
    """指定の game_id の game summary が、なければ新規作成、あれば更新します."""
    _create_not_existing_team(game_summary_data.get('home_team_id'), game_summary_data.pop('home_team_abb', None))
    _create_not_existing_team(game_summary_data.get('away_team_id'), game_summary_data.pop('away_team_abb', None))

    game_id = game_summary_data.get("game_id")

    if game_id:
        if GameSummary.objects.filter(game_id=game_id).exists():
            instance = GameSummary.objects.get(game_id=game_id)
        else:
            instance = None
        serializer = GameSummarySerializer(instance=instance, data=game_summary_data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors)
    else:
        raise ValueError('game ID is None or undefined')


def _create_not_existing_team(team_id: int, team_abb: str):
    if not Team.objects.filter(team_id=team_id).exists():
        serializer = TeamSerializer(data={
            'team_id': team_id,
            'abbreviation': team_abb,
            'logo': _fetch_and_encode_svg(f'https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg')
        })
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(serializer.errors)


def _fetch_and_encode_svg(url: str) -> str:
    base = 'data:image/svg+xml;base64,'
    if url == '':
        return base
    else:
        try:
            cached_response = cache.get(url)
            if cached_response:
                return cached_response
            response = requests.get(url)
            response.raise_for_status()
            svg_bytes = response.content
            b64 = base64.b64encode(svg_bytes).decode('utf-8')
            cache.set(url, base + b64, timeout=60*10)
            return base + b64
        except:
            return base

