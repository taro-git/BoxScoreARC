from typing import List, TypedDict

from rest_framework import serializers

from rest_api.models.season_summary import RegularSeasonTeamStats, SeasonSummary


##
## schema for access from django self
####
class RegularSeasonTeamStatsCreate(TypedDict):
    team_id: int
    conference: str
    conference_rank: int
    division: str
    division_rank: int
    win: int
    lose: int
    pts: int
    ast: int
    stl: int
    blk: int
    fg: int
    fga: int
    three: int
    threea: int
    ft: int
    fta: int
    oreb: int
    dreb: int
    to: int
    pf: int
    plusminus: int


class SeasonSummaryCreate(TypedDict):
    season: str
    teams: List[RegularSeasonTeamStatsCreate]


##
## Serializer
####
class RegularSeasonTeamStatsSerializer(serializers.ModelSerializer):
    reb = serializers.SerializerMethodField(read_only=True)
    eff = serializers.SerializerMethodField(read_only=True)
    team_abbreviation = serializers.SerializerMethodField(read_only=True)
    team_logo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RegularSeasonTeamStats
        fields = [
            "team_id",
            "conference",
            "conference_rank",
            "division",
            "division_rank",
            "win",
            "lose",
            "pts",
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
            "reb",
            "eff",
            "team_abbreviation",
            "team_logo",
        ]

    def get_reb(self, obj):
        return obj.reb

    def get_eff(self, obj):
        return obj.eff

    def get_team_abbreviation(self, obj):
        return obj.team_abbreviation

    def get_team_logo(self, obj):
        return obj.team_logo


class SeasonSummarySerializer(serializers.ModelSerializer):
    teams = RegularSeasonTeamStatsSerializer(
        many=True, source="regular_season_team_stats", required=False, allow_empty=True
    )

    class Meta:
        model = SeasonSummary
        fields = "__all__"

    def get_game_category(self, obj):
        return obj.game_category

    def create(self, validated_data):
        regular_season_teams_data = validated_data.pop("regular_season_team_stats", [])
        season = SeasonSummary.objects.create(**validated_data)
        for regular_season_team_data in regular_season_teams_data:
            RegularSeasonTeamStats.objects.create(season=season, **regular_season_team_data)
        return season

    def update(self, instance, validated_data):
        regular_season_teams_data = validated_data.pop("regular_season_team_stats", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if regular_season_teams_data is not None:
            instance.regular_stats.all().delete()
            for regular_season_team_data in regular_season_teams_data:
                RegularSeasonTeamStats.objects.create(season=instance, **regular_season_team_data)

        return instance
