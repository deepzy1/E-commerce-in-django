# Generated by Django 5.1 on 2024-09-27 09:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0009_ordereditems"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderedItems2",
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
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=20)),
                ("product_names", models.JSONField()),
                ("quantities", models.JSONField()),
                ("prices", models.JSONField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-order_date"],
            },
        ),
        migrations.DeleteModel(
            name="OrderedItems",
        ),
    ]
