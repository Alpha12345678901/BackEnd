# Generated by Django 4.0.6 on 2022-07-22 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save_moves', '0006_alter_chessgamelog_options_chessgamelog_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessgamelog',
            name='turn',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]