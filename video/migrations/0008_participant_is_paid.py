# Generated by Django 4.2.16 on 2025-01-02 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0007_participant_temp_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
