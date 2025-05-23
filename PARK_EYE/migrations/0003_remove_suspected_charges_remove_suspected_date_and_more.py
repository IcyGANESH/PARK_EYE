# Generated by Django 5.2 on 2025-05-09 22:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PARK_EYE', '0002_vehiclerecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suspected',
            name='charges',
        ),
        migrations.RemoveField(
            model_name='suspected',
            name='date',
        ),
        migrations.AddField(
            model_name='suspected',
            name='crime_attempted',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suspected',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='suspected',
            name='found_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suspected',
            name='is_founded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suspected',
            name='spotted_location',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclerecord',
            name='in_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
