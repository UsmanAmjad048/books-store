# Generated by Django 5.0.3 on 2024-04-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0015_alter_cartitem_seller_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='seller_id',
            field=models.CharField(max_length=20),
        ),
    ]
