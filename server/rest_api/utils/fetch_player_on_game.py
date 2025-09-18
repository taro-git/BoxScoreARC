from typing import List, TypedDict

from nba_api.stats.endpoints import boxscoreplayertrackv3, boxscoresummaryv2

from rest_api.models.game_summary import GameSummary, PlayerOnGame
from rest_api.serializers.game_summary import PlayerOnGameCreate


class PlayersDict(TypedDict):
    home_team_id: int
    home_players: List[PlayerOnGameCreate]
    away_team_id: int
    away_players: List[PlayerOnGameCreate]


def fetch_player_on_game(game_id: str) -> PlayersDict:
    """指定のgame_id の選手情報を返します.
    DBに各チーム8人以上のプレイヤーが登録済みであれば、DB の値を返します."""
    if GameSummary.objects.filter(game_id=game_id).exists():
        game_summary_existing_db = GameSummary.objects.get(game_id=game_id)
        home_team_id = game_summary_existing_db.home_team.team_id
        away_team_id = game_summary_existing_db.away_team.team_id
    else:
        game_summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id).game_summary.get_data_frame()
        home_team_id = game_summary["HOME_TEAM_ID"].iloc[0]
        away_team_id = game_summary["VISITOR_TEAM_ID"].iloc[0]
    players_existing_db = PlayerOnGame.objects.filter(game_id=game_id)
    home_players: List[PlayerOnGameCreate] = []
    away_players: List[PlayerOnGameCreate] = []
    for player_existing_db in players_existing_db:
        player_on_game_create = PlayerOnGameCreate(
            {
                "player_id": player_existing_db.player_id,
                "name": player_existing_db.name,
                "jersey": player_existing_db.jersey,
                "position": player_existing_db.position,
                "is_starter": player_existing_db.is_starter,
                "is_inactive": player_existing_db.is_inactive,
                "sequence": player_existing_db.sequence,
            }
        )
        if player_existing_db.is_home:
            home_players.append(player_on_game_create)
        else:
            away_players.append(player_on_game_create)
    if len(home_players) < 8 or len(away_players) < 8:
        home_players: List[PlayerOnGameCreate] = []
        away_players: List[PlayerOnGameCreate] = []
        try:
            box_score_summary_v2 = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
            inactive_players = box_score_summary_v2.inactive_players.get_data_frame()
            line_score = box_score_summary_v2.line_score.get_data_frame()
            home_team_abbreviation = line_score[line_score["TEAM_ID"] == home_team_id]["TEAM_ABBREVIATION"].iloc[0]
            box_score_player_track_v3 = boxscoreplayertrackv3.BoxScorePlayerTrackV3(game_id=game_id)
            player_stats = box_score_player_track_v3.player_stats.get_data_frame()
            for player in player_stats.itertuples():
                player_on_game_create = PlayerOnGameCreate(
                    {
                        "player_id": int(player.personId),
                        "name": player.nameI,
                        "jersey": player.jerseyNum,
                        "position": player.position,
                        "is_inactive": False,
                    }
                )
                if player.teamId == home_team_id:
                    player_on_game_create["is_starter"] = len(home_players) < 5
                    player_on_game_create["sequence"] = len(home_players) + 1
                    home_players.append(player_on_game_create)
                else:
                    player_on_game_create["is_starter"] = len(away_players) < 5
                    player_on_game_create["sequence"] = len(away_players) + 1
                    away_players.append(player_on_game_create)
            for inactive_player in inactive_players.itertuples():
                player_on_game_create = PlayerOnGameCreate(
                    {
                        "player_id": inactive_player.PLAYER_ID,
                        "name": " ".join([inactive_player.FIRST_NAME, inactive_player.LAST_NAME]),
                        "jersey": inactive_player.JERSEY_NUM,
                        "position": "",
                        "is_starter": False,
                        "is_inactive": True,
                    }
                )
                if inactive_player.TEAM_ABBREVIATION == home_team_abbreviation:
                    player_on_game_create["sequence"] = len(home_players) + 1
                    home_players.append(player_on_game_create)
                else:
                    player_on_game_create["sequence"] = len(away_players) + 1
                    away_players.append(player_on_game_create)
        except Exception:
            pass
    return {
        "home_team_id": home_team_id,
        "home_players": home_players,
        "away_team_id": away_team_id,
        "away_players": away_players,
    }
