from django.db import IntegrityError, transaction
from nba_api.stats.endpoints.teaminfocommon import TeamInfoCommon

from rest_api.models.season_summary import SeasonSummary
from rest_api.serializers.season_summary import (
    RegularSeasonTeamStatsCreate,
    SeasonSummaryCreate,
    SeasonSummarySerializer,
)


##
## Fetch from nba_api
####
def fetch_regular_season_team_stats(season: str, team_id: int) -> RegularSeasonTeamStatsCreate:
    """nba_api から指定の season, team_id の RegularSeasonTeamStatsCreate クラスを作成します."""
    team_info = TeamInfoCommon(team_id=str(team_id), season_nullable=season)
    team_info_common = team_info.team_info_common.get_data_frame()
    team_season_ranks = team_info.team_season_ranks.get_data_frame()
    win = int(team_info_common["W"].iloc[0])
    lose = int(team_info_common["L"].iloc[0])
    if season == team_info_common["SEASON_YEAR"].iloc[0]:
        return {
            "team_id": int(team_info_common["TEAM_ID"].iloc[0]),
            "conference": team_info_common["TEAM_CONFERENCE"].iloc[0],
            "conference_rank": int(team_info_common["CONF_RANK"].iloc[0]),
            "division": team_info_common["TEAM_DIVISION"].iloc[0],
            "division_rank": int(team_info_common["DIV_RANK"].iloc[0]),
            "win": win,
            "lose": lose,
            "pts": int((win + lose) * team_season_ranks["PTS_PG"].iloc[0]),
            "ast": int((win + lose) * team_season_ranks["AST_PG"].iloc[0]),
            "stl": 0,
            "blk": 0,
            "fg": 0,
            "fga": 0,
            "three": 0,
            "threea": 0,
            "ft": 0,
            "fta": 0,
            "oreb": 0,
            "dreb": 0,
            "to": 0,
            "pf": 0,
            "plusminus": 0,
        }
    else:
        raise ValueError(
            f"not match season, request value is {season}, responce value is {team_info_common['SEASON_YEAR'].iloc[0]}"
        )


##
## Upsert to DB
####
def upsert_season_summary(season_summary_create: SeasonSummaryCreate):
    """指定の season の season summary が、なければ新規作成、あれば更新します."""

    season = season_summary_create.get("season")
    if not season:
        raise ValueError("Season is not set")

    try:
        with transaction.atomic():
            instance = SeasonSummary.objects.filter(season=season).first()
            serializer = SeasonSummarySerializer(instance=instance, data=season_summary_create)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
    except IntegrityError as e:
        raise ValueError(f"DB制約違反: {e}")
    except ValueError as ve:
        raise ve
