# Generated by Django 5.0.1 on 2024-02-29 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("announcement", "0002_announcement_price_announcementimage_preview_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
    ]