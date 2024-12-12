# Generated by Django 5.1 on 2024-12-10 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs_management", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="name",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="date",
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name="room",
            name="building",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="room",
            name="number",
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="student",
            name="name",
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
