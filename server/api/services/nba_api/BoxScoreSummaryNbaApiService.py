from datetime import datetime, timedelta

from nba_api.stats.endpoints import boxscoretraditionalv2, boxscoresummaryv2, boxscoreplayertrackv3

from ...models.nba_api.BoxScoreSummaryModel import Player, TeamSummary, BoxScoreSummary

class BoxScoreSummaryNbaApiService:
    def __init__(self):
        pass

    def get_box_score_summary(self, game_id: str) -> BoxScoreSummary:
        box_score_summary_v2 = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
        inactive_players = box_score_summary_v2.inactive_players.get_data_frame()
        game_summary = box_score_summary_v2.game_summary.get_data_frame()
        line_score = box_score_summary_v2.line_score.get_data_frame()
        box_score_player_track_v3 = boxscoreplayertrackv3.BoxScorePlayerTrackV3(game_id=game_id)
        player_stats = box_score_player_track_v3.player_stats.get_data_frame()

        home_team_id = game_summary["HOME_TEAM_ID"].iloc[0]
        away_team_id = game_summary["VISITOR_TEAM_ID"].iloc[0]
        home_team_abbreviation = line_score[line_score["TEAM_ID"] == home_team_id]["TEAM_ABBREVIATION"].iloc[0]
        away_team_abbreviation = line_score[line_score["TEAM_ID"] == away_team_id]["TEAM_ABBREVIATION"].iloc[0]
        game_date_est_str = line_score["GAME_DATE_EST"].iloc[0]
        game_date_jst = datetime.fromisoformat(game_date_est_str).date() + timedelta(days=1)

        inactive_player_ids = set(inactive_players["PLAYER_ID"])
        home_players = []
        away_players = []
        for player in player_stats.itertuples():
            if player.teamId == home_team_id:
                home_players.append(
                    Player(
                        player_id=int(player.personId),
                        name=player.nameI,
                        jersey=player.jerseyNum,
                        position=player.position,
                        is_inactive=player.personId in inactive_player_ids,
                        sequence=len(home_players)+1
                    )
                )
            else:
                away_players.append(
                    Player(
                        player_id=int(player.personId),
                        name=player.nameI,
                        jersey=player.jerseyNum,
                        position=player.position,
                        is_inactive=player.personId in inactive_player_ids,
                        sequence=len(away_players)+1
                    )
                )
        home_players = sorted(home_players, key=lambda player: (player.is_inactive, player.sequence))
        away_players = sorted(away_players, key=lambda player: (player.is_inactive, player.sequence))
        home_team = TeamSummary(
            team_id=int(home_team_id),
            abbreviation=home_team_abbreviation,
            players=home_players
        )
        away_team = TeamSummary(
            team_id=int(away_team_id),
            abbreviation=away_team_abbreviation,
            players=away_players
        )
        return BoxScoreSummary(
            game_date_jst=game_date_jst,
            home= home_team,
            away=away_team
        )


        