# Generated by Django 2.0.2 on 2018-05-09 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0005_institution_identity_provider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='identity_provider_login',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='identity_provider_logout',
        ),
    ]