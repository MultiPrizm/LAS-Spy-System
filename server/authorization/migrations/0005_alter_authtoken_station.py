# Generated by Django 5.1.2 on 2024-12-29 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_workstation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='station',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='authorization.workstation'),
        ),
    ]
