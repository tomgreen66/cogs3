# Generated by Django 2.1.4 on 2019-08-02 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0027_institution_needs_priority_workflow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='local_mailing_list_link',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='local_mailing_list_name',
        ),
    ]
