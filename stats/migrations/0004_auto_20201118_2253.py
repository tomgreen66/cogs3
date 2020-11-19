# Generated by Django 2.2.13 on 2020-11-18 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20201118_2249'),
        ('stats', '0003_auto_20201118_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklystatstorageprojectscf',
            name='phase',
        ),
        migrations.AddField(
            model_name='weeklystatstorageprojectscf',
            name='system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.System'),
        ),
    ]