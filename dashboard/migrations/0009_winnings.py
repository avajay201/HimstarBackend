# Generated by Django 4.2.16 on 2024-12-09 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_register_custom_id_alter_register_dob_and_more'),
        ('dashboard', '0008_competition_stage_tournament_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winnings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.register')),
            ],
        ),
    ]
