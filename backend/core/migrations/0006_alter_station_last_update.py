# Generated by Django 4.0.3 on 2022-04-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_station_last_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="station",
            name="last_update",
            field=models.DateTimeField(null=True),
        ),
    ]
