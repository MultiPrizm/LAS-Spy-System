# Generated by Django 5.1.4 on 2025-01-04 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spy_app', '0010_browserhistoryitem_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browserhistoryitem',
            name='time',
            field=models.TextField(max_length=32, null=True),
        ),
    ]
