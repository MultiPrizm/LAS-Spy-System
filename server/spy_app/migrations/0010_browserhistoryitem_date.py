# Generated by Django 5.1.4 on 2025-01-04 16:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spy_app', '0009_browserhistoryitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='browserhistoryitem',
            name='date',
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
    ]
