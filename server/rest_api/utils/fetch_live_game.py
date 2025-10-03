import re
from datetime import datetime
from typing import TypedDict

from nba_api.live.nba.endpoints import BoxScore, boxscore

from rest_api.models.game_summary import GameSummary
from rest_api.serializers.box_score import BoxScoreCreate
from rest_api.serializers.game_summary import GameSummaryCreate
from rest_api.utils.make_box_score_create import BoxScoreCreateMaker


class LiveGameDict(TypedDict):
    game_summary_create: GameSummaryCreate
    box_score_create: BoxScoreCreate


def fetch_live_game(game_summary: GameSummary) -> LiveGameDict:
    """nba_api をたたいて、ライブの試合の GameSummaryCreate と BoxScoreCreate を作成します.
    GameSummaryCreate の status id は常に 2 (試合中) を返します."""
    box_score = boxscore.BoxScore(game_id=game_summary.game_id)
    return {
        "game_summary_create": _make_game_summary_create(box_score, game_summary),
        "box_score_create": _make_box_score_create(box_score, game_summary),
    }


def _make_game_summary_create(box_score: BoxScore, game_summary: GameSummary) -> GameSummaryCreate:
    game_details = box_score.game_details.get_dict()
    home_team_stats = box_score.home_team_stats.get_dict()
    home_team_player_stats = box_score.home_team_player_stats.get_dict()
    away_team_stats = box_score.away_team_stats.get_dict()
    away_team_player_stats = box_score.away_team_player_stats.get_dict()
    return {
        "game_id": game_summary.game_id,
        "home_team_id": game_summary.home_team.team_id,
        "home_team_abb": game_summary.home_team.abbreviation,
        "home_score": home_team_stats["score"],
        "home_players": sorted(
            [
                {
                    "player_id": player["personId"],
                    "name": player["nameI"],
                    "jersey": player["jerseyNum"],
                    "position": player.get("position", ""),
                    "is_starter": player["starter"] == "1",
                    "is_inactive": not player["status"] == "ACTIVE",
                    "sequence": player["order"],
                }
                for player in home_team_player_stats
            ],
            key=lambda player: player["sequence"],
        ),
        "away_team_id": game_summary.away_team.team_id,
        "away_team_abb": game_summary.away_team.abbreviation,
        "away_score": away_team_stats["score"],
        "away_players": sorted(
            [
                {
                    "player_id": player["personId"],
                    "name": player["nameI"],
                    "jersey": player["jerseyNum"],
                    "position": player.get("position", ""),
                    "is_starter": player["starter"] == "1",
                    "is_inactive": not player["status"] == "ACTIVE",
                    "sequence": player["order"],
                }
                for player in away_team_player_stats
            ],
            key=lambda player: player["sequence"],
        ),
        "game_datetime": datetime.fromisoformat(game_details["gameTimeLocal"]),
        "status_id": 2,
        "status_text": game_details["gameStatusText"],
        "sequence": game_summary.sequence,
    }


def _make_box_score_create(box_score: BoxScore, game_summary: GameSummary) -> BoxScoreCreate:
    box_score_create_maker = BoxScoreCreateMaker(game_summary.game_id, 0, [], [])

    keys = [
        "sec",
        "pts",
        "reb",
        "ast",
        "stl",
        "blk",
        "fg",
        "fga",
        "three",
        "threea",
        "ft",
        "fta",
        "oreb",
        "dreb",
        "to",
        "pf",
        "plusminus",
    ]

    def _update_box_score_data_values(is_home: bool, plyaers_stats: dict, team_stats: dict) -> None:
        for player in plyaers_stats:
            box_score_create_maker.append_box_score_data(
                0,
                player["personId"],
                is_home,
                keys,
                [
                    _calc_play_time(player["statistics"]["minutes"]),
                    player["statistics"]["points"],
                    player["statistics"]["reboundsTotal"],
                    player["statistics"]["assists"],
                    player["statistics"]["steals"],
                    player["statistics"]["blocks"],
                    player["statistics"]["fieldGoalsMade"],
                    player["statistics"]["fieldGoalsAttempted"],
                    player["statistics"]["threePointersMade"],
                    player["statistics"]["threePointersAttempted"],
                    player["statistics"]["freeThrowsMade"],
                    player["statistics"]["freeThrowsAttempted"],
                    player["statistics"]["reboundsOffensive"],
                    player["statistics"]["reboundsDefensive"],
                    player["statistics"]["turnovers"],
                    player["statistics"]["foulsPersonal"],
                    int(player["statistics"]["plusMinusPoints"]),
                ],
            )
            if not player["oncourt"] == "1":
                box_score_create_maker.players_to_bench(0, 0, [player["personId"]], is_home)
        box_score_create_maker.append_box_score_data(
            0,
            team_stats["teamId"],
            is_home,
            keys,
            [
                0,
                0,
                team_stats["statistics"]["reboundsTeam"],
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                team_stats["statistics"]["reboundsTeamOffensive"],
                team_stats["statistics"]["reboundsTeamDefensive"],
                team_stats["statistics"]["turnoversTeam"],
                0,
                0,
            ],
        )

    _update_box_score_data_values(
        True,
        box_score.home_team_player_stats.get_dict(),
        box_score.home_team_stats.get_dict(),
    )
    _update_box_score_data_values(
        False,
        box_score.away_team_player_stats.get_dict(),
        box_score.away_team_stats.get_dict(),
    )
    return box_score_create_maker.to_box_score_create()


def _calc_play_time(playtime_str: str) -> int:
    match = re.match(r"PT(\d+)M(\d+(\.\d+)?)S", playtime_str)

    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return int(minutes * 60 + seconds)
    else:
        raise ValueError("Invalid playtime format in live box score")
