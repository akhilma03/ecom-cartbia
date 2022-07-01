# Generated by Django 4.0.4 on 2022-06-23 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_delete_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('discount_percentage', models.FloatField()),
                ('discount_from', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
