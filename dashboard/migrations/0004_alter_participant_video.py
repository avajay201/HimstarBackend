# Generated by Django 4.2.16 on 2024-11-16 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_competition_file_uri_tournament_file_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='competition_videos/'),
        ),
    ]