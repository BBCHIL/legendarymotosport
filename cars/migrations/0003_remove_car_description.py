# Generated by Django 3.2.9 on 2021-11-29 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_alter_car_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='description',
        ),
    ]
