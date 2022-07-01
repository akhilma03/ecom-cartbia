# Generated by Django 4.0.4 on 2022-06-30 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_product_filter_price_delete_filter_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('pricerange_from', models.IntegerField(null=True)),
                ('pricerange_to', models.IntegerField(null=True)),
            ],
        ),
    ]
