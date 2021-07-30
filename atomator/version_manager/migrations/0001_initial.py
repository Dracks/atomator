# Generated by Django 3.0.6 on 2020-06-02 08:13

# Django imports
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Build",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("major", models.PositiveIntegerField()),
                ("minor", models.PositiveIntegerField()),
                ("patch", models.PositiveIntegerField()),
                ("commit", models.CharField(max_length=255)),
                ("release", models.BooleanField(default=False)),
                (
                    "change",
                    models.IntegerField(
                        choices=[(0, "Major"), (1, "Minor"), (2, "Patch")]
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="application.Application",
                    ),
                ),
            ],
            options={"ordering": ("-date",),},
        ),
        migrations.CreateModel(
            name="FileInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("size", models.PositiveIntegerField()),
                ("file_name", models.CharField(max_length=256)),
                ("content_type", models.CharField(max_length=256)),
                (
                    "build",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="file",
                        to="version_manager.Build",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Change",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("fix", "Fix"),
                            ("imp", "Improvement"),
                            ("fea", "New Feature"),
                            ("unk", "Unknown"),
                        ],
                        max_length=3,
                        null=True,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "build",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="changes_list",
                        to="version_manager.Build",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="build",
            index=models.Index(
                fields=["major", "minor"], name="version_man_major_d3fe41_idx"
            ),
        ),
    ]