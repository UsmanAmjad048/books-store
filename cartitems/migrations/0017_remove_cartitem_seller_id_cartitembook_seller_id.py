# Generated by Django 5.0.3 on 2024-04-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartitems', '0016_alter_cartitem_seller_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='seller_id',
        ),
        migrations.AddField(
            model_name='cartitembook',
            name='seller_id',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
