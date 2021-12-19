# Generated by Django 3.2.9 on 2021-11-30 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PREPARING', 'PREPARING'), ('SHIPPING', 'SHIPPING'), ('AWAITS', 'AWAITS'), ('DELIVERED', 'DELIVERED')], default='PREPARING', max_length=25),
        ),
    ]