# Generated by Django 3.2.9 on 2021-11-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(null=True, upload_to='static/img/account/uploaded'),
        ),
    ]
