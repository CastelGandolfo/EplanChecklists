# Generated by Django 3.1 on 2020-08-25 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0005_eplan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]