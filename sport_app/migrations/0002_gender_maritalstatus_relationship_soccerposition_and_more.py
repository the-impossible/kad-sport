# Generated by Django 5.0.2 on 2024-02-20 15:14

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sport_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gender",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gender_title", models.CharField(max_length=20)),
            ],
            options={"verbose_name_plural": "Genders", "db_table": "Gender",},
        ),
        migrations.CreateModel(
            name="MaritalStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name_plural": "Marital Status",
                "db_table": "Marital Status",
            },
        ),
        migrations.CreateModel(
            name="Relationship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name_plural": "Relationships",
                "db_table": "Relationship",
            },
        ),
        migrations.CreateModel(
            name="SoccerPosition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name_plural": "Soccer Position",
                "db_table": "Soccer Position",
            },
        ),
        migrations.CreateModel(
            name="Screening",
            fields=[
                (
                    "screening_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("age", models.CharField(max_length=3)),
                ("date_of_birth", models.DateField()),
                ("present_weight", models.CharField(max_length=10)),
                ("present_height", models.CharField(max_length=10)),
                (
                    "medical_condition",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "present_weakness",
                    models.CharField(
                        blank=True,
                        help_text="(Speed, skills, shooting ability, heading, passes, control etc)",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("next_of_kin", models.CharField(max_length=30)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("date_applied", models.DateTimeField(auto_now_add=True)),
                (
                    "gender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sport_app.gender",
                    ),
                ),
                (
                    "marital_status",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sport_app.maritalstatus",
                    ),
                ),
                (
                    "relationship",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sport_app.relationship",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "soccer_position",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sport_app.soccerposition",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Screening", "db_table": "Screening",},
        ),
    ]