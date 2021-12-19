from django.db import models
from django.db.models.enums import Choices

class Order(models.Model):
    STATUS = (
        ('PREPARING', 'PREPARING'),
        ('SHIPPING', 'SHIPPING'),
        ('AWAITS', 'AWAITS'),
        ('DELIVERED', 'DELIVERED'),
    )
    car = models.ForeignKey(
        'cars.Car', on_delete=models.CASCADE,
        related_name='orders',
    )
    user = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE,
        related_name='orders',
    )
    manufacturer = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE,
        related_name='user_orders',
    )
    color = models.CharField(max_length=25)
    status = models.CharField(
        choices=STATUS,
        default='PREPARING',
        max_length=25,
    )