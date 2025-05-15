from typing import List, Dict, Literal
from datetime import datetime, timedelta

from ...models.nba_api.GameIdsModel import get_game_ids_by_est_date
from ...models.nba_api.GameSummariesModel import get_game_summaries
from ..common.TimeDiffAdjustService import convert_jst_to_est, convert_est_to_jst

GameStatus = Literal["SCHEDULED", "PLAYING", "FINAL"]

def get_games(jst_date_str: str) -> List[Dict]:
    jst_date = datetime.strptime(jst_date_str, "%Y%m%d")
    est_date = convert_jst_to_est(jst_date)
    est_date_yesterday = est_date - timedelta(days=1)

    game_ids_today = get_game_ids_by_est_date(est_date.strftime("%Y-%m-%d"))
    game_ids_yesterday = get_game_ids_by_est_date(est_date_yesterday.strftime("%Y-%m-%d"))
    all_game_ids = list(set(game_ids_today + game_ids_yesterday))

    summaries = get_game_summaries(all_game_ids)

    result = []
    for game in summaries:
        start_time_jst = convert_est_to_jst(game.start_time_est)
        if start_time_jst.date() == jst_date.date():
            result.append({
                "game_id": game.game_id,
                "home_team": game.home_team,
                "away_team": game.away_team,
                "start_time_jst": start_time_jst.isoformat(),
                "status": normalize_game_status(game.status_id),
                "live_period": game.live_period,
                "live_clock": game.live_clock,
            })
    return result

def normalize_game_status(status_id: str) -> GameStatus:
    if status_id == 3:
        return 'FINAL'
    elif status_id == 1:
        return 'SCHEDULED'
    else:
        return 'PLAYING'
