# Generated by Django 5.1 on 2024-08-26 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0004_delete_histogram"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="display_summary_statistics",
            field=models.BooleanField(default=False),
        ),
    ]