# Generated by Django 4.0.4 on 2022-06-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_reviewrating_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter_price',
            name='price',
        ),
        migrations.AddField(
            model_name='filter_price',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='filter_price',
            name='pricerange_from',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filter_price',
            name='pricerange_to',
            field=models.IntegerField(null=True),
        ),
    ]
