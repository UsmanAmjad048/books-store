# Generated by Django 5.0.3 on 2024-04-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0003_remove_cartitem_shipping_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='shipping_method',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
