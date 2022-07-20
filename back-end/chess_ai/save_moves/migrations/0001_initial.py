# Generated by Django 4.0.6 on 2022-07-19 18:12

import django.contrib.postgres.fields
from django.db import migrations, models
import save_moves.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessGameLog',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('whiteAgentName', models.CharField(max_length=1000)),
                ('blackAgentName', models.CharField(max_length=1000)),
                ('timeControl', models.CharField(default='N/A', max_length=100)),
                ('moves', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=save_moves.models.get_moves_default, size=None)),
                ('timeTracker', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=save_moves.models.get_time_tracker_default, size=None)),
                ('result', models.CharField(default='ongoing', max_length=100)),
                ('numberOfMoves', models.PositiveIntegerField(default=0)),
                ('whiteMaterialLeftCurrent', models.PositiveIntegerField(default=39)),
                ('blackMaterialLeftCurrent', models.PositiveIntegerField(default=39)),
                ('materialDifferenceCurrent', models.IntegerField(default=0)),
                ('whiteTimeLeftCurrent', models.CharField(default='N/A', max_length=100)),
                ('blackTimeLeftCurrent', models.CharField(default='N/A', max_length=100)),
                ('whiteMoveLast', models.CharField(max_length=100)),
                ('blackMoveLast', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]