from django.db import models
from django.db.models.fields.related import ForeignKey

class Like(models.Model):
    user = ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE,
        related_name='likes',
    )
    car = ForeignKey(
        'cars.Car', on_delete=models.CASCADE,
        related_name='likes',
    )

class Favorite(models.Model):
    user = ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE,
        related_name='favorites',
    )
    car = ForeignKey(
        'cars.Car', on_delete=models.CASCADE,
        related_name='favorites',
    )