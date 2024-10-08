# Generated by Django 5.1 on 2024-08-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0002_cart_cartitem"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="total_price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="slug",
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
