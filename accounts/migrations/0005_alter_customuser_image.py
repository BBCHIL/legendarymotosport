# Generated by Django 3.2.9 on 2021-12-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_is_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='/static/img/account/user.png', upload_to='uploaded/accounts'),
        ),
    ]
