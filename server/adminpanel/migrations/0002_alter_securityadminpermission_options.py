# Generated by Django 5.1.4 on 2025-01-01 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='securityadminpermission',
            options={'permissions': [('security_admin', 'Can access Security Admin Panel'), ('work_admin', 'Can access Work Admin Panel')]},
        ),
    ]
