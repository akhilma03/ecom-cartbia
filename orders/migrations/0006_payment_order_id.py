# Generated by Django 4.0.4 on 2022-06-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_payment_payment_method_cod'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]