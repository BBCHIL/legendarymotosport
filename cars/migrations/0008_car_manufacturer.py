# Generated by Django 3.2.9 on 2021-12-16 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0007_alter_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='accounts.customuser'),
            preserve_default=False,
        ),
    ]
