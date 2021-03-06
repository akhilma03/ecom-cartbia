# Generated by Django 4.0.4 on 2022-06-08 03:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images1',
            field=models.ImageField(default=datetime.datetime(2022, 6, 8, 3, 56, 9, 161281, tzinfo=utc), upload_to='photos/product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='images2',
            field=models.ImageField(default=datetime.datetime(2022, 6, 8, 3, 56, 19, 137249, tzinfo=utc), upload_to='photos/product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='images3',
            field=models.ImageField(default=datetime.datetime(2022, 6, 8, 3, 56, 27, 121210, tzinfo=utc), upload_to='photos/product'),
            preserve_default=False,
        ),
    ]
