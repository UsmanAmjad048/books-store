# Generated by Django 5.0.3 on 2024-04-16 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='sellerid',
            new_name='seller_id',
        ),
    ]
