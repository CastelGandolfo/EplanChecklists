# Generated by Django 3.1 on 2020-08-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0003_auto_20200823_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='eplan_count',
            field=models.IntegerField(default=0),
        ),
    ]
