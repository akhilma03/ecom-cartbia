# Generated by Django 4.0.4 on 2022-06-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method_cod',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
