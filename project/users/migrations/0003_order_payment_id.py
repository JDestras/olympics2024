# Generated by Django 5.0.4 on 2024-05-28 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
