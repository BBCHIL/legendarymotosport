# Generated by Django 3.2.9 on 2021-12-07 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_manufacturer',
            field=models.BooleanField(default=False),
        ),
    ]
