# Generated by Django 5.0.3 on 2024-03-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_remove_bookstore_due_date_bookstore_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookstore',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]
