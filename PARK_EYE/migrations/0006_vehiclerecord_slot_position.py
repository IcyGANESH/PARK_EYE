# Generated by Django 5.2.1 on 2025-05-10 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PARK_EYE", "0005_location_remove_police_location_police_locations"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehiclerecord",
            name="slot_position",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
