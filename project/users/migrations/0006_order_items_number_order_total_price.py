# Generated by Django 5.0.4 on 2024-05-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_order_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
