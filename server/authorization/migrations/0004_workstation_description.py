# Generated by Django 5.1.2 on 2024-12-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0003_authtoken_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='workstation',
            name='description',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
