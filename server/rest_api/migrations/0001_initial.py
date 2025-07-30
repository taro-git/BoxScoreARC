import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameSummary',
            fields=[
                ('game_id', models.CharField(primary_key=True, serialize=False)),
                ('sequence', models.IntegerField()),
                ('status_id', models.IntegerField()),
                ('status_text', models.CharField()),
                ('live_period', models.IntegerField()),
                ('live_clock', models.CharField()),
                ('game_date_est', models.DateField()),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('abbreviation', models.CharField()),
                ('logo', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='BoxScore',
            fields=[
                ('game_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rest_api.gamesummary')),
            ],
        ),
        migrations.AddField(
            model_name='gamesummary',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_games', to='rest_api.team'),
        ),
        migrations.AddField(
            model_name='gamesummary',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_games', to='rest_api.team'),
        ),
        migrations.CreateModel(
            name='BoxScorePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_home', models.BooleanField()),
                ('player_id', models.IntegerField()),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='rest_api.boxscore')),
            ],
        ),
        migrations.CreateModel(
            name='BoxScoreData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elapsed_seconds', models.IntegerField()),
                ('is_on_court', models.BooleanField()),
                ('min', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pts', models.IntegerField()),
                ('reb', models.IntegerField()),
                ('ast', models.IntegerField()),
                ('stl', models.IntegerField()),
                ('blk', models.IntegerField()),
                ('fg', models.IntegerField()),
                ('fga', models.IntegerField()),
                ('fgper', models.DecimalField(decimal_places=2, max_digits=5)),
                ('three', models.IntegerField()),
                ('threea', models.IntegerField()),
                ('threeper', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ft', models.IntegerField()),
                ('fta', models.IntegerField()),
                ('ftper', models.DecimalField(decimal_places=2, max_digits=5)),
                ('oreb', models.IntegerField()),
                ('dreb', models.IntegerField()),
                ('to', models.IntegerField()),
                ('pf', models.IntegerField()),
                ('eff', models.DecimalField(decimal_places=2, max_digits=5)),
                ('plusminus', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment_data', to='rest_api.boxscoreplayer')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('player', 'elapsed_seconds'), name='unique_box_score_player_id_elapsed_seconds')],
            },
        ),
        migrations.CreateModel(
            name='PlayerOnGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_home', models.BooleanField()),
                ('player_id', models.IntegerField()),
                ('name', models.CharField()),
                ('jersey', models.CharField(blank=True, null=True)),
                ('position', models.CharField(blank=True, null=True)),
                ('is_starter', models.BooleanField()),
                ('is_inactive', models.BooleanField()),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='rest_api.gamesummary')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('game_id', 'player_id'), name='unique_game_summary_game_id_player_id')],
            },
        ),
        migrations.AddConstraint(
            model_name='boxscoreplayer',
            constraint=models.UniqueConstraint(fields=('game_id', 'player_id'), name='unique_box_score_game_id_player_id'),
        ),
    ]
