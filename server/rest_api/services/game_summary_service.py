import base64
import re
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

import requests
from django.core.cache import cache
from django.db import IntegrityError, transaction
from nba_api.stats.endpoints import leaguegamefinder, scheduleleaguev2, scoreboardv2

from rest_api.models.game_summary import GameSummary, Team
from rest_api.serializers.game_summary import (
    GameSummaryCreate,
    GameSummarySerializer,
    TeamSerializer,
)
from rest_api.utils.fetch_player_on_game import fetch_player_on_game


##
## Fetch from nba_api
####
def fetch_game_summaries_by_season(
    season: str | None = None,
) -> List[GameSummaryCreate]:
    """nba_api から指定のシーズンの GameSummaryCreate クラスを生成します.
    指定がない場合、現在のシーズン (10/1から次シーズン) を扱います.
    players 情報は含まれません."""
    # 2017-18 シーズン以降のデータしかない. leaguegamefinder だと 1997 年くらいまである
    schedule_league = None
    try:
        schedule_league = (
            scheduleleaguev2.ScheduleLeagueV2(season=season) if season else scheduleleaguev2.ScheduleLeagueV2()
        )
    except Exception:
        print("leaguegamefinder")
        league_game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season, league_id_nullable="00")
    if schedule_league:
        season_games = schedule_league.season_games.get_data_frame()
        game_summary_creates: List[GameSummaryCreate] = []
        for season_game in season_games.itertuples():
            game_summary_creates.append(
                {
                    "game_id": season_game.gameId,
                    "home_team_id": season_game.homeTeam_teamId,
                    "home_team_abb": season_game.homeTeam_teamTricode
                    if season_game.homeTeam_teamTricode
                    else "unknown",
                    "home_score": season_game.homeTeam_score if season_game.homeTeam_score else 0,
                    "home_players": [],
                    "away_team_id": season_game.awayTeam_teamId,
                    "away_team_abb": season_game.awayTeam_teamTricode
                    if season_game.awayTeam_teamTricode
                    else "unknown",
                    "away_score": season_game.awayTeam_score if season_game.awayTeam_score else 0,
                    "away_players": [],
                    "game_datetime": datetime.strptime(season_game.gameDateTimeEst, "%Y-%m-%dT%H:%M:%SZ").replace(
                        tzinfo=ZoneInfo("America/New_York")
                    ),
                    "status_id": season_game.gameStatus,
                    "status_text": season_game.gameStatusText if season_game.gameStatusText else "Final",
                    "sequence": season_game.gameSequence,
                }
            )
    else:
        league_game_finder_results = league_game_finder.league_game_finder_results.get_data_frame()
        game_summary_creates: List[GameSummaryCreate] = []
        game_ids = league_game_finder_results["GAME_ID"].drop_duplicates().tolist()
        for game_id in game_ids:
            teams_for_game = league_game_finder_results[league_game_finder_results["GAME_ID"] == game_id]
            game_date = datetime.strptime(teams_for_game["GAME_DATE"].iloc[0], "%Y-%m-%d")
            if len(teams_for_game) == 2:
                matchup_str = teams_for_game["MATCHUP"].iloc[0]
                if "vs." in matchup_str:
                    home_team_abbreviation = matchup_str[:3]
                elif "@" in matchup_str:
                    home_team_abbreviation = matchup_str[-3:]
                else:
                    raise ValueError(f"String of MATCHUP {matchup_str} in GAME_ID {game_id} does not contain vs. or @.")
                home_team = teams_for_game[teams_for_game["TEAM_ABBREVIATION"] == home_team_abbreviation]
                away_team = teams_for_game[teams_for_game["TEAM_ABBREVIATION"] != home_team_abbreviation]
                if len(home_team) != 1 or len(away_team) != 1:
                    game_summary_creates.append(
                        {
                            "game_id": game_id,
                            "home_team_id": -1,
                            "home_team_abb": "unknown",
                            "home_score": 0,
                            "home_players": [],
                            "away_team_id": -2,
                            "away_team_abb": "unknown",
                            "away_score": 0,
                            "away_players": [],
                            "game_datetime": datetime(
                                game_date.year,
                                game_date.month,
                                game_date.day,
                                11,
                                0,
                                0,
                                tzinfo=ZoneInfo("America/New_York"),
                            ),
                            "status_id": 3 if game_date < datetime.now() else 1,
                            "status_text": "Final" if game_date < datetime.now() else "h:mm pm/am ET",
                            "sequence": 100,
                        }
                    )
                    continue
            else:
                game_summary_creates.append(
                    {
                        "game_id": game_id,
                        "home_team_id": -1,
                        "home_team_abb": "unknown",
                        "home_score": 0,
                        "home_players": [],
                        "away_team_id": -2,
                        "away_team_abb": "unknown",
                        "away_score": 0,
                        "away_players": [],
                        "game_datetime": datetime(
                            game_date.year,
                            game_date.month,
                            game_date.day,
                            11,
                            0,
                            0,
                            tzinfo=ZoneInfo("America/New_York"),
                        ),
                        "status_id": 3 if game_date < datetime.now() else 1,
                        "status_text": "Final" if game_date < datetime.now() else "h:mm pm/am ET",
                        "sequence": 100,
                    }
                )
                continue
            game_summary_creates.append(
                {
                    "game_id": game_id,
                    "home_team_id": home_team["TEAM_ID"].iloc[0],
                    "home_team_abb": home_team["TEAM_ABBREVIATION"].iloc[0]
                    if home_team["TEAM_ABBREVIATION"].iloc[0]
                    else "unknown",
                    "home_score": home_team["PTS"].iloc[0] if home_team["PTS"].iloc[0] else 0,
                    "home_players": [],
                    "away_team_id": away_team["TEAM_ID"].iloc[0],
                    "away_team_abb": away_team["TEAM_ABBREVIATION"].iloc[0]
                    if away_team["TEAM_ABBREVIATION"].iloc[0]
                    else "unknown",
                    "away_score": away_team["PTS"].iloc[0] if away_team["PTS"].iloc[0] else 0,
                    "away_players": [],
                    "game_datetime": datetime(
                        game_date.year,
                        game_date.month,
                        game_date.day,
                        11,
                        0,
                        0,
                        tzinfo=ZoneInfo("America/New_York"),
                    ),
                    "status_id": 3 if game_date < datetime.now() else 1,
                    "status_text": "Final" if game_date < datetime.now() else "h:mm pm/am ET",
                    "sequence": 1,
                }
            )
    return game_summary_creates


def fetch_game_summaries_by_date(date_est: datetime | None) -> List[GameSummaryCreate]:
    """nba_api から指定の日付の GameSummaryCreate クラスを生成します.
    指定がない場合、実行当日を扱います.
    players 情報は含まれません."""
    today_est = datetime.now(ZoneInfo("America/New_York"))
    game_date = date_est if date_est else today_est
    scoreboard = scoreboardv2.ScoreboardV2(game_date=game_date)
    game_header = scoreboard.game_header.get_data_frame()
    line_score = scoreboard.line_score.get_data_frame()

    game_summaries: List[GameSummaryCreate] = []
    game_ids = game_header["GAME_ID"].tolist()

    for game_id in game_ids:
        filtered_game_header = game_header[game_header["GAME_ID"] == game_id][
            [
                "GAME_STATUS_ID",
                "GAME_STATUS_TEXT",
                "LIVE_PERIOD",
                "LIVE_PC_TIME",
                "HOME_TEAM_ID",
            ]
        ]
        filtered_line_score = line_score[line_score["GAME_ID"] == game_id][
            ["GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS", "TEAM_ID"]
        ]
        home_team_line_score = filtered_line_score[
            filtered_line_score["TEAM_ID"] == filtered_game_header["HOME_TEAM_ID"].iloc[0]
        ]
        away_team_line_score = filtered_line_score[
            filtered_line_score["TEAM_ID"] != filtered_game_header["HOME_TEAM_ID"].iloc[0]
        ]
        home_score = home_team_line_score["PTS"].iloc[0]
        away_score = away_team_line_score["PTS"].iloc[0]
        game_summaries.append(
            {
                "game_id": game_id,
                "home_team_id": home_team_line_score["TEAM_ID"].iloc[0],
                "home_team_abb": home_team_line_score["TEAM_ABBREVIATION"].iloc[0],
                "home_score": home_score if home_score else 0,
                "home_players": [],
                "away_team_id": away_team_line_score["TEAM_ID"].iloc[0],
                "away_team_abb": away_team_line_score["TEAM_ABBREVIATION"].iloc[0],
                "away_score": away_score if away_score else 0,
                "away_players": [],
                "game_datetime": _add_time_info_to_game_date(
                    filtered_game_header["GAME_STATUS_ID"].iloc[0],
                    filtered_game_header["GAME_STATUS_TEXT"].iloc[0],
                    datetime(
                        game_date.year,
                        game_date.month,
                        game_date.day,
                        11,
                        0,
                        0,
                        tzinfo=ZoneInfo("America/New_York"),
                    ),
                ),
                "status_id": filtered_game_header["GAME_STATUS_ID"].iloc[0],
                "status_text": filtered_game_header["GAME_STATUS_TEXT"].iloc[0],
                "sequence": filtered_line_score["GAME_SEQUENCE"].iloc[0],
            }
        )

    return game_summaries


def update_players_in_game_summary_by_game_id(game_id: str) -> GameSummaryCreate:
    """players 情報を更新した GameSummaryCreate クラスを作成します.
    DB 上の GameSumamry に players 情報があれば、nba_api は使用せず、そのままの値を使います."""
    try:
        game_summary_from_db: GameSummary = GameSummary.objects.get(game_id=game_id)
    except Exception:
        raise ValueError("error in update_game_summary_by_game_id: game id {game_id} is not in db")
    players = fetch_player_on_game(game_id)
    return GameSummaryCreate(
        {
            "game_id": game_id,
            "home_team_id": game_summary_from_db.home_team.team_id,
            "home_team_abb": game_summary_from_db.home_team.abbreviation,
            "home_score": game_summary_from_db.home_score,
            "home_players": players["home_players"],
            "away_team_id": game_summary_from_db.away_team.team_id,
            "away_team_abb": game_summary_from_db.away_team.abbreviation,
            "away_score": game_summary_from_db.away_score,
            "away_players": players["away_players"],
            "game_datetime": _add_time_info_to_game_date(
                game_summary_from_db.status_id,
                game_summary_from_db.status_text,
                game_summary_from_db.game_datetime,
            ),
            "status_id": game_summary_from_db.status_id,
            "status_text": game_summary_from_db.status_text,
            "sequence": game_summary_from_db.sequence,
        }
    )


def get_regular_season_team_ids_by_season(season: str) -> List[int]:
    """DB から指定の season でレギュラーシーズンの試合を実施した実績のある team_id 一覧を返します."""
    game_summaries = GameSummary.objects.all()
    season_finised_game_summaries = [
        game_summary
        for game_summary in game_summaries
        if game_summary.season == season and game_summary.game_category == "Regular Season"
    ]
    team_ids: list[int] = []
    for season_finished_game_summary in season_finised_game_summaries:
        team_ids.append(season_finished_game_summary.home_team.team_id)
        team_ids.append(season_finished_game_summary.away_team.team_id)
    return list(set(team_ids))


def _add_time_info_to_game_date(status_id: int, status_text: str, game_date: datetime) -> datetime:
    """status_text を基にgame_date に時間情報を付加します.
    付加すべき情報が無かった場合や時間情報の取得に失敗した場合はそのままの日付情報を返します."""
    if status_id == 1:
        status_text = status_text.strip()
        formatted_time_str = re.match(r"(\d{1,2}:\d{2}\s*(am|pm))\s*ET", status_text, re.IGNORECASE)
        if not formatted_time_str:
            return game_date
        game_time = datetime.strptime(
            f"{datetime.now().date()} {formatted_time_str.group(1).lower()}",
            "%Y-%m-%d %I:%M %p",
        ).replace(tzinfo=game_date.tzinfo)
        game_datetime = game_time.replace(year=game_date.year, month=game_date.month, day=game_date.day)
    else:
        game_datetime = game_date
    return game_datetime


##
## Upsert to DB
####
def upsert_game_summary(game_summary_create: GameSummaryCreate):
    """指定の game_id の game summary が、なければ新規作成、あれば更新します."""
    _create_not_existing_team(
        game_summary_create.get("home_team_id", -1),
        str(game_summary_create.pop("home_team_abb", "unknown")),
    )
    _create_not_existing_team(
        game_summary_create.get("away_team_id", -2),
        str(game_summary_create.pop("away_team_abb", "unknown")),
    )

    game_id = game_summary_create.get("game_id")
    if not game_id:
        raise ValueError("Game ID is not set")

    try:
        with transaction.atomic():
            instance = GameSummary.objects.filter(game_id=game_id).first()
            serializer: GameSummarySerializer = GameSummarySerializer(instance=instance, data=game_summary_create)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
    except IntegrityError as e:
        raise ValueError(f"DB制約違反: {e}")
    except ValueError as ve:
        raise ve


def _create_not_existing_team(team_id: int, team_abb: str):
    if not Team.objects.filter(team_id=team_id).exists():
        try:
            with transaction.atomic():
                serializer = TeamSerializer(
                    data={
                        "team_id": team_id,
                        "abbreviation": team_abb,
                        "logo": _fetch_and_encode_svg(f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"),
                    }
                )
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
        except IntegrityError as e:
            raise ValueError(f"DB制約違反: {e}")
        except ValueError as ve:
            raise ve


def _fetch_and_encode_svg(url: str) -> str:
    base = "data:image/svg+xml;base64,"
    if url == "":
        return base
    else:
        try:
            cached_response = cache.get(url)
            if cached_response:
                return cached_response
            response = requests.get(url)
            response.raise_for_status()
            svg_bytes = response.content
            b64 = base64.b64encode(svg_bytes).decode("utf-8")
            cache.set(url, base + b64, timeout=60 * 10)
            return base + b64
        except Exception:
            return base
