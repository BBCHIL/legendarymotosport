# Generated by Django 3.2.9 on 2021-12-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_car_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.PositiveBigIntegerField(),
        ),
    ]