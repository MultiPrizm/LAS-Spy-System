# Generated by Django 5.1.4 on 2025-01-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spy_app', '0005_alter_dailyworkreport_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworkreport',
            name='finish_time',
            field=models.TextField(max_length=30000, null=True),
        ),
    ]
