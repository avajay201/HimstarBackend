# Generated by Django 4.2.16 on 2024-12-12 18:10

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_winnings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='is_online',
        ),
        migrations.RemoveField(
            model_name='competition',
            name='parent_tournament',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='is_online',
        ),
        migrations.AddField(
            model_name='tournament',
            name='competitions',
            field=models.ManyToManyField(related_name='tournaments', to='dashboard.competition'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.category'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='price',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='rules',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]