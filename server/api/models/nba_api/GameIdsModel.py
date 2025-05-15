from nba_api.stats.endpoints import scoreboardv2


def get_game_ids_by_est_date(est_date_str: str) -> list:
    scoreboard = scoreboardv2.ScoreboardV2(game_date=est_date_str)
    df = scoreboard.game_header.get_data_frame()
    return df["GAME_ID"].tolist()
