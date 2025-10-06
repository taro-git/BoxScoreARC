from copy import deepcopy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.utils.timezone import make_aware

from rest_api.models.box_score import BoxScore
from rest_api.models.game_summary import GameSummary
from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus
from rest_api.services.box_score_service import fetch_box_score, upsert_box_score
from rest_api.services.game_summary_service import (
    update_players_in_game_summary_by_game_id,
    upsert_game_summary,
)
from rest_api.utils.fetch_live_game import fetch_live_game
from rest_api.utils.fetch_player_on_game import fetch_player_on_game


def update_live_games_job(scheduler: BackgroundScheduler):
    """日次で 00:00 に実行する処理を定義します.
    当日に予定されている試合がある場合に、game summary と box score を定期更新します."""
    print("[scheduler] add daily job: live game")
    scheduler.add_job(
        func=lambda: _update_live_games_job(scheduler),
        trigger=CronTrigger(hour=0, minute=0),
        id="update_live_games_job",
        next_run_time=datetime.now(),
        replace_existing=True,
    )


def _update_live_games_job(scheduler: BackgroundScheduler):
    """当日に予定されている試合がある場合に、game summary および box score の定期更新用ジョブを追加します."""
    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    game_summaries = GameSummary.objects.filter(
        game_datetime__range=(make_aware(today), make_aware(today + timedelta(minutes=60 * 24 - 1))),
    ).exclude(status_id=3)
    for game_summary in game_summaries:
        job_id = f"update_live_box_score_{game_summary.game_id}"
        game_datetime = game_summary.game_datetime.astimezone(ZoneInfo("Asia/Tokyo"))
        print(
            f"[scheduler] add job ({job_id}) whitch is every 10 minutes "
            f"from {game_datetime}: live game "
            f"({game_summary.home_team.abbreviation} vs. {game_summary.away_team.abbreviation})"
        )
        scheduler.add_job(
            func=lambda jid=deepcopy(job_id), gid=deepcopy(game_summary.game_id): _update_live_game_job(
                scheduler, jid, gid
            ),
            trigger=IntervalTrigger(minutes=10),
            id=deepcopy(job_id),
            next_run_time=deepcopy(game_datetime),
            replace_existing=True,
        )
    return


def _update_live_game_job(scheduler: BackgroundScheduler, job_id: str, game_id: str):
    """box score を定期更新します."""
    print(f"[scheduler] start update job at {datetime.now()}: {job_id}")
    game_summary = GameSummary.objects.filter(game_id=game_id).first()
    if game_summary is not None:
        match_up = f"{game_summary.home_team.abbreviation} vs. {game_summary.away_team.abbreviation}"
        if not game_summary.status_text.startswith("Final"):
            print(f"[scheduler] try fetch and upsert live game, {match_up}")
            try:
                live_game = fetch_live_game(game_summary)
            except Exception as e:
                print(f"[scheduler] error in fetch_live_game, {match_up}. {e}")
            try:
                upsert_game_summary(live_game["game_summary_create"])
            except Exception as e:
                print(f"[scheduler] error in live upsert_game_summary, {match_up}. {e}")
            try:
                upsert_box_score(live_game["box_score_create"])
            except Exception as e:
                print(f"[scheduler] error in upsert_box_score, {match_up}. {e}")
        else:
            print(f"[scheduler] try fetch and upsert box score of finished game, {match_up}")
            status = ScheduledBoxScoreStatus.objects.filter(game_id=game_id).first()
            box_score = BoxScore.objects.filter(game_id=game_id).first()
            if status is None or status.status == "errored" or box_score is None or not box_score.is_collect:
                print(
                    f"[scheduler] not collect or error in fetch and upsert box score of finished game, {match_up}."
                    f" so retry"
                )
                try:
                    game_summary_create = update_players_in_game_summary_by_game_id(game_id)
                except Exception as e:
                    print(f"[scheduler] error in update_players_in_game_summary_by_game_id, {match_up}. {e}")
                try:
                    box_score_create = fetch_box_score(game_id)
                except Exception as e:
                    print(f"[scheduler] error in fetch_box_score, {match_up}. {e}")
                try:
                    home_score = sum([p["box_score_data"][-1]["pts"] for p in box_score_create["home_players"]])
                    away_score = sum([p["box_score_data"][-1]["pts"] for p in box_score_create["away_players"]])
                    if (
                        home_score == game_summary_create["home_score"]
                        and away_score == game_summary_create["away_score"]
                    ):
                        upsert_game_summary(game_summary_create)
                        upsert_box_score(box_score_create)
                    else:
                        raise ValueError(
                            f"score is not match."
                            f" from game summary:"
                            f" {game_summary_create['away_score']} - {game_summary_create['home_score']}"
                            f" from box score: {away_score} - {home_score}"
                        )
                except Exception as e:
                    print(f"[scheduler] error in upsert_game_summary and upsert_box_score, {match_up}. {e}")
            elif status.status == "completed" and box_score.is_collect:
                try:
                    players = fetch_player_on_game(game_id)
                    upsert_game_summary(
                        {
                            "game_id": game_id,
                            "home_team_id": game_summary.home_team.team_id,
                            "home_team_abb": game_summary.home_team.abbreviation,
                            "home_score": game_summary.home_score,
                            "home_players": players["home_players"],
                            "away_team_id": game_summary.away_team.team_id,
                            "away_team_abb": game_summary.away_team.abbreviation,
                            "away_score": game_summary.away_score,
                            "away_players": players["away_players"],
                            "game_datetime": game_summary.game_datetime,
                            "status_id": 3,
                            "status_text": game_summary.status_text,
                            "sequence": game_summary.sequence,
                        }
                    )
                    print(f"[scheduler] remove {job_id}")
                    scheduler.remove_job(job_id)
                except Exception as e:
                    print(f"[scheduler] error in final upsert_game_summary, {match_up}. {e}")
    return
