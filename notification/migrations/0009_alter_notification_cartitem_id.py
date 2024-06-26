# Generated by Django 5.0.3 on 2024-04-19 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0017_remove_cartitem_seller_id_cartitembook_seller_id'),
        ('notification', '0008_alter_notification_cartitem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='cartitem_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cartitems_id', to='cartitems.cartitem'),
            preserve_default=False,
        ),
    ]
