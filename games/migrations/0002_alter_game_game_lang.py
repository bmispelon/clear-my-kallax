# Generated by Django 4.0.4 on 2022-05-01 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_lang',
            field=models.CharField(choices=[('FR', 'French'), ('EN', 'English'), ('HU', 'Hungarian'), ('XX', 'Language independent')], default='XX', max_length=2),
        ),
    ]
