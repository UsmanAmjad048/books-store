# Generated by Django 5.0.3 on 2024-04-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_alter_notification_cartitem_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='cartitem_id',
            field=models.CharField(max_length=1000),
        ),
    ]
