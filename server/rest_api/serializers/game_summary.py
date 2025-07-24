from rest_framework import serializers

from ..models.game_summary import GameSummary


class GameSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSummary
        fields = '__all__'

    def validate(self, data):
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        game_id = data.get('game_id')

        errors = {}

        if home_team.game_id != game_id:
            errors['home_team'] = "Home team must belong to this game."
        if away_team.game_id != game_id:
            errors['away_team'] = "Away team must belong to this game."

        if home_team.team_id == away_team.team_id:
            errors['team_id'] = "Home and away teams must be different."

        if not home_team.is_home:
            errors['home_team'] = "Home team must have is_home=True."
        if away_team.is_home:
            errors['away_team'] = "Away team must have is_home=False."

        if errors:
            raise serializers.ValidationError(errors)

        return data
