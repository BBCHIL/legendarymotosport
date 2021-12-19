from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from favorites.models import Favorite, Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

    def like(self, user, car):
        try:
            Like.objects.get(
                user=user, car=car,
            ).delete()
        except ObjectDoesNotExist:
            Like.objects.create(
                user=user, car=car,
            )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
    
    def validate(self, attrs):
        return super().validate(attrs)