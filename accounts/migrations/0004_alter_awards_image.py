# Generated by Django 4.2.16 on 2024-11-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_awards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awards',
            name='image',
            field=models.ImageField(upload_to='awards'),
        ),
    ]
