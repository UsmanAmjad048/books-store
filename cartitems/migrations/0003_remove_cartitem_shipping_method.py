# Generated by Django 5.0.3 on 2024-04-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0002_remove_cartitem_color_remove_cartitem_coupon_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='shipping_method',
        ),
    ]