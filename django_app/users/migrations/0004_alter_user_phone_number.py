# Generated by Django 5.0.1 on 2024-02-29 19:11

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_date_joined_user_is_active_user_is_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                default=None,
                max_length=20,
                null=True,
                region=None,
                verbose_name="Phone number",
            ),
        ),
    ]