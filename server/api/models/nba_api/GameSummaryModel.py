from typing import Literal
from dataclasses import dataclass

TeamAbbreviation = Literal[
    'ORL', 'ATL', 'CHA', 'BOS', 'NYK', 'BKN', 'IND', 'CLE', 'WAS', 'MIA', 'CHI', 'PHI', 'DET', 'MIL', 'TOR',
    'DEN', 'HOU', 'DAL', 'MEM', 'UTA', 'MIN', 'OKC', 'NOP', 'SAS', 'LAC', 'GSW', 'LAL', 'POR', 'PHX', 'SAC'
]

@dataclass
class GameSummary:
    game_id: str
    home_team: TeamAbbreviation
    home_score: int
    away_team: TeamAbbreviation
    away_score: int
    game_sequence: int
    status_id: int
    status_text: str
    live_period: int
    live_clock: str


# def get_game_summaries(game_ids: List[str]) -> List[GameSummary]:
#     scoreboard = scoreboardv2.ScoreboardV2(game_date=game_date_str)
#     game_header = scoreboard.game_header.get_data_frame()
#     game_header_keys = ["GAME_ID", "GAME_STATUS_ID", "GAME_STATUS_TEXT", "LIVE_PERIOD", "LIVE_PC_TIME"]
#     line_score = scoreboard.line_score.get_data_frame()
#     line_score_keys = ["GAME_ID", "GAME_SEQUENCE", "TEAM_ABBREVIATION", "PTS"]
#     summaries = []

#     for game_id in game_ids:
#         boxscore = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
#         game_summary_df = boxscore.game_summary.get_data_frame()
#         line_score_df = boxscore.line_score.get_data_frame()

#         if game_summary_df.empty or line_score_df.empty:
#             continue

#         game_date = game_summary_df.loc[0, 'GAME_DATE_EST']
#         status_id = game_summary_df.loc[0, 'GAME_STATUS_ID']
#         if status_id == 1:
#             game_time = game_summary_df.loc[0, 'GAME_STATUS_TEXT']
#             start_time_est = combine_date_and_time(game_date, game_time)
#         else:
#             start_time_est = combine_date_and_time(game_date, '8:00 pm ET')

#         period = game_summary_df.loc[0].get('LIVE_PERIOD')
#         if period not in [1, 2, 3, 4]:
#             period = None
#         clock = game_summary_df.loc[0].get('LIVE_PC_TIME')

#         home_team = ''
#         home_score = 0
#         away_team = ''
#         away_score = 0
#         for _, row in line_score_df.iterrows():
#             if row['TEAM_ID'] == game_summary_df.loc[0, 'HOME_TEAM_ID']:
#                 home_team = row['TEAM_ABBREVIATION']
#                 home_score = row['PTS']
#             else:
#                 away_team = row['TEAM_ABBREVIATION']
#                 away_score = row['PTS']

#         summaries.append(GameSummary(
#             game_id=game_id,
#             home_team=home_team,
#             home_score=home_score,
#             away_team=away_team,
#             away_score=away_score,
#             start_time=start_time_est,
#             status_id=status_id,
#             status=None,
#             live_period=period,
#             live_clock=clock if isinstance(clock, str) else None
#         ))

#     return summaries
