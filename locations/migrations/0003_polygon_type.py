# Generated by Django 4.0.2 on 2022-02-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0002_rename_points_polygon_coordinates"),
    ]

    operations = [
        migrations.AddField(
            model_name="polygon",
            name="type",
            field=models.CharField(default="Polygon", editable=False, max_length=7),
        ),
    ]
