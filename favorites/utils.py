from django.contrib.auth.models import AnonymousUser
from favorites.models import Like

def car_like_exists(user, car):
    return Like.objects.filter(user=user, car=car).exists() if not isinstance(user, AnonymousUser) else False