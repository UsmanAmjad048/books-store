# Generated by Django 5.0.3 on 2024-03-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_remove_bookstore_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookstore',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
