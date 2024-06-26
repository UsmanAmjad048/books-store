# Generated by Django 5.0.3 on 2024-04-16 12:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cartitems', '0013_cartitembook_booktitle'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('cartitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartitems.cartitem')),
                ('cartitembook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartitems.cartitembook')),
                ('purchaserid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_as_purchaser', to=settings.AUTH_USER_MODEL)),
                ('sellerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_as_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
