from django.db import models
from django.db.models.fields.related import ForeignKey

class Car(models.Model):
    name = models.CharField(
        max_length=60
    )
    # User that has permission to create cars
    manufacturer = ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE,
        related_name='cars',
    )
    price = models.PositiveBigIntegerField()

    image = models.ImageField(
        upload_to='uploaded/cars',
    )
    description = models.TextField()

    def get_short_name(self):
        return '{}...'.format(self.name[:14])


    def dollarize(self) -> str:
        """
        Changing price from 1000000 to $1,000,000 
        """
        return "${:,}".format(self.price)
