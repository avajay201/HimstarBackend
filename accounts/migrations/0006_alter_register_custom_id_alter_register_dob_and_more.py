# Generated by Django 4.2.16 on 2024-11-30 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_points_required_awards_votes_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='custom_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\d{10,15}$')]),
        ),
        migrations.AlterField(
            model_name='register',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
