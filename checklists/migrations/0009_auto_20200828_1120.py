# Generated by Django 3.1 on 2020-08-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0008_auto_20200825_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistpoint',
            name='user_edited',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='selectedcheckpoint',
            name='user_edited',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]