# Generated by Django 5.0.3 on 2024-04-01 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0005_remove_cartitem_shipping_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price_per_item',
        ),
    ]