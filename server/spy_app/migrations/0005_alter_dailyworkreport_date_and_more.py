# Generated by Django 5.1.4 on 2025-01-02 15:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spy_app', '0004_remove_dailyworkreport_data_dailyworkreport_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkreport',
            name='date',
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
        migrations.AlterField(
            model_name='dailyworkreport',
            name='finish_time',
            field=models.TimeField(null=True),
        ),
    ]
