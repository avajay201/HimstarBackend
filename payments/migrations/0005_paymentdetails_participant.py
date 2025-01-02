# Generated by Django 4.2.16 on 2025-01-02 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_participant_is_paid'),
        ('payments', '0004_paymentdetails_competition_paymentdetails_tournament_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdetails',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='video.participant'),
        ),
    ]