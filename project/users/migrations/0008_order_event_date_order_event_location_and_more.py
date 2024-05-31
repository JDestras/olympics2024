# Generated by Django 5.0.4 on 2024-05-31 15:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_order_items_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='event_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='event_location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='event_sport',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='event_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
