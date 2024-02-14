# Generated by Django 5.0.1 on 2024-02-08 20:18

import core.utils
import phonenumber_field.modelfields
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="updated"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "type",
                    models.IntegerField(
                        choices=[
                            (0, "Administrator"),
                            (1, "Common user"),
                            (2, "Moderator"),
                        ],
                        verbose_name="Type",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=30, null=True, unique=True, verbose_name="Username"
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default=None,
                        max_length=20,
                        null=True,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to=core.utils.get_storage_path
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CommonUser",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.user",),
            managers=[
                ("objects", users.models.RegularUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ModeratorUser",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.user",),
            managers=[
                ("objects", users.models.ModeratorUserManager()),
            ],
        ),
    ]