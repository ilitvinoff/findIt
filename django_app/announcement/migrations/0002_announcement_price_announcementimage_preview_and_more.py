# Generated by Django 5.0.1 on 2024-02-22 08:15

import core.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("announcement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="announcement",
            name="price",
            field=models.FloatField(default=0, verbose_name="Price"),
        ),
        migrations.AddField(
            model_name="announcementimage",
            name="preview",
            field=models.ImageField(
                blank=True,
                storage=core.utils.select_storage,
                upload_to=core.utils.get_storage_path,
            ),
        ),
        migrations.AlterField(
            model_name="announcement",
            name="content",
            field=models.CharField(
                max_length=1200, null=True, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="announcement",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="descendants",
                to="announcement.category",
            ),
        ),
    ]
