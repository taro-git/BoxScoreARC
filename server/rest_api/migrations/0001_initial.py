import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoxScorePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_home', models.BooleanField()),
                ('player_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameSummary',
            fields=[
                ('game_id', models.CharField(primary_key=True, serialize=False)),
                ('sequence', models.IntegerField()),
                ('status_id', models.IntegerField()),
                ('status_text', models.CharField()),
                ('game_datetime', models.DateTimeField()),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SchedulerLock',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False)),
                ('locked_at', models.DateTimeField(auto_now=True)),
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
            name='BoxScoreData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elapsed_seconds', models.IntegerField()),
                ('is_on_court', models.BooleanField()),
                ('sec', models.IntegerField()),
                ('pts', models.IntegerField()),
                ('reb', models.IntegerField()),
                ('ast', models.IntegerField()),
                ('stl', models.IntegerField()),
                ('blk', models.IntegerField()),
                ('fg', models.IntegerField()),
                ('fga', models.IntegerField()),
                ('three', models.IntegerField()),
                ('threea', models.IntegerField()),
                ('ft', models.IntegerField()),
                ('fta', models.IntegerField()),
                ('oreb', models.IntegerField()),
                ('dreb', models.IntegerField()),
                ('to', models.IntegerField()),
                ('pf', models.IntegerField()),
                ('plusminus', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moment_data', to='rest_api.boxscoreplayer')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledBoxScoreStatus',
            fields=[
                ('game_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rest_api.gamesummary')),
                ('registered_datetime', models.DateTimeField(auto_now=True)),
                ('error_message', models.CharField(blank=True, null=True)),
                ('progress', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
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
            name='BoxScore',
            fields=[
                ('game_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rest_api.scheduledboxscorestatus')),
                ('final_seconds', models.IntegerField()),
            ],
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
        migrations.AddField(
            model_name='boxscoreplayer',
            name='game_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='rest_api.boxscore'),
        ),
        migrations.AddConstraint(
            model_name='boxscoreplayer',
            constraint=models.UniqueConstraint(fields=('game_id', 'player_id'), name='unique_box_score_game_id_player_id'),
        ),
    ]
