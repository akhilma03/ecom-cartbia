# Generated by Django 4.0.4 on 2022-06-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_cartitems_variations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(choices=[('100 TO 500', '500 TO 1000'), ('1000 TO 1500', '1500 TO 2000'), ('2000 TO 2500', '2500 TO 3000'), ('3000 TO 3500', '3500 TO 4000'), ('4000 TO 4500', '4500 TO 5000')], max_length=60, null=True)),
            ],
        ),
    ]
