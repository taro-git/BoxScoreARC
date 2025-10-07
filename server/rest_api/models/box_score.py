from typing import TypedDict

from django.db import models

from rest_api.models.game_summary import GameSummary


class _TeamStats(TypedDict):
    score: int
    playing_time_sum: int
    plusminus_sum: int


class BoxScore(models.Model):
    game_id = models.OneToOneField(GameSummary, primary_key=True, on_delete=models.CASCADE)
    final_seconds = models.IntegerField()

    @property
    def final_period(self):
        return 4 + round((self.final_seconds - 4 * 12 * 60) / (5 * 60))

    def _calc_team_stats(self, players) -> _TeamStats:
        sec = 0
        pts = 0
        plusminus = 0
        for player in players:
            final_data = player.moment_data.last()
            if final_data:
                sec += final_data.sec
                pts += final_data.pts
                plusminus += final_data.plusminus
        return {
            "score": pts,
            "playing_time_sum": sec,
            "plusminus_sum": plusminus,
        }

    @property
    def home_stats(self) -> _TeamStats:
        return self._calc_team_stats(self.home_players_on_box_score)

    @property
    def away_stats(self) -> _TeamStats:
        return self._calc_team_stats(self.away_players_on_box_score)

    @property
    def is_collect(self):
        return (
            (self.home_stats["score"] - self.away_stats["score"]) * 5 == self.home_stats["plusminus_sum"]
            and self.home_stats["plusminus_sum"] + self.away_stats["plusminus_sum"] == 0
            and self.final_seconds * 5 == self.home_stats["playing_time_sum"]
            and self.final_seconds * 5 == self.away_stats["playing_time_sum"]
            and self.final_period >= 4
        )

    @property
    def home_players_on_box_score(self):
        return self.players.filter(is_home=True)

    @property
    def away_players_on_box_score(self):
        return self.players.filter(is_home=False)


class BoxScorePlayer(models.Model):
    game_id = models.ForeignKey(BoxScore, on_delete=models.CASCADE, related_name="players")
    is_home = models.BooleanField()
    player_id = models.IntegerField()

    @property
    def data(self):
        return self.moment_data.order_by("elapsed_seconds")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game_id", "player_id"],
                name="unique_box_score_game_id_player_id",
            )
        ]


class BoxScoreData(models.Model):
    player = models.ForeignKey(BoxScorePlayer, on_delete=models.CASCADE, related_name="moment_data")
    elapsed_seconds = models.IntegerField()
    is_on_court = models.BooleanField()
    sec = models.IntegerField()

    @property
    def min(self):
        return round(self.sec / 60, 1)

    pts = models.IntegerField()
    reb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    fg = models.IntegerField()
    fga = models.IntegerField()
    three = models.IntegerField()
    threea = models.IntegerField()
    ft = models.IntegerField()
    fta = models.IntegerField()
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    to = models.IntegerField()
    pf = models.IntegerField()
    plusminus = models.IntegerField()

    @property
    def eff(self):
        return (self.pts + self.reb + self.ast + self.stl + self.blk) - (
            (self.fga - self.fg) + (self.fta - self.ft) + self.to
        )
