# Generated by Django 2.0.2 on 2018-07-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180619_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reason_for_account',
            field=models.TextField(blank=True, max_length=1024, verbose_name='Reason for account'),
        ),
    ]
