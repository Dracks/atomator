# Generated by Django 3.0.6 on 2020-06-17 11:15

# Django imports
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0002_auto_20200617_1115"),
        ("deployment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="taskoutput", options={"ordering": ("-id",)},
        ),
        migrations.AddField(
            model_name="executionoutput",
            name="application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="application.Application",
            ),
        ),
        migrations.AlterField(
            model_name="taskoutput",
            name="status",
            field=models.SmallIntegerField(
                choices=[
                    (0, "Nothing done"),
                    (1, "Changed"),
                    (2, "Error"),
                    (3, "Unreachable"),
                ]
            ),
        ),
    ]
