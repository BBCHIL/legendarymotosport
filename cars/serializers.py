import re
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser
from accounts.utils import get_user
from cars.models import Car
from favorites.models import Favorite
from favorites.utils import car_like_exists
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from legendarymotosports.utils import delete_files, prepare_form_data

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
    
    @staticmethod
    def get_from_favorites(query):
        """
        Returns car list, used in 
        """
        return list(map(lambda fav_obj: Car.objects.get(id=fav_obj.car_id), query))

    @staticmethod
    def prepare_render(query, user=None, many=False):
        """
        Making some model values more readable, putting some additional data.
        able to change a single object, and a whole query.
        """
        def perform_changes(obj):
            obj.price = obj.dollarize()
            obj.like_count = obj.likes.count()
            obj.like_exists = car_like_exists(user, obj)
            if len(obj.name) > 14 and many: # many needs to not shortify name in detail view
                obj.name = obj.get_short_name()
            return obj
        if many:
            for obj in query:
                perform_changes(obj)
        else:
            perform_changes(query)
            if not isinstance(user, AnonymousUser) and user is not None:
                user.is_owner = query.manufacturer.id == user.id
                query.in_favorites = Favorite.objects.filter(user=user, car=query).exists()
        return query



class CarCreateSerializer(serializers.Serializer):

    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    image = serializers.ImageField()
    manufacturer_id = serializers.IntegerField()

    @staticmethod
    def get_data(request):
        data = prepare_form_data(request.data)
        data['manufacturer_id'] = get_user(request).id # required field
        return data

    def validate(self, attrs):
        name = attrs.get('name')
        description = attrs.get('description')
        price = attrs.get('price')
        manufacturer_id = attrs.pop('manufacturer_id')

        errors = {}

        if not name:
            msg = '*name was not provided'
            errors['name'] = msg
        
        if not price or price < 0:
            msg = '*price is negative number or was not provided'
            errors['price'] = msg

        if not description:
            msg = '*description was not provided'
            errors['descrption'] = msg
        
        if manufacturer_id:
            try:
                attrs['manufacturer'] = CustomUser.objects.get(id=manufacturer_id)
            except ObjectDoesNotExist:
                errors['other'] = 'User Error: user was not found'
        else:
            errors['other'] = 'User Error: user was not found'

        if errors:
            self.validation_errors = errors
            raise serializers.ValidationError()


        return super().validate(attrs)


class CarEditSerializer(serializers.Serializer):

    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.IntegerField(required=False, allow_null=True)
    image = serializers.ImageField(required=False)
    manufacturer_id = serializers.IntegerField()

    @staticmethod
    def get_data(request):
        data = CarCreateSerializer.get_data(request)
        data = dict(filter(lambda items: bool(items[1]), data.items())) # removing keys with no value
        return data
    
    @staticmethod
    def put_changes(car, data):
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image = data.get('image')

        if name:
            car.name = name
        if description:
            car.description = description
        if price:
            car.price = price
        if image:
            delete_files(car)
            car.image = image
        car.save()


    def validate(self, attrs):
        name = attrs.get('name')
        description = attrs.get('description')
        price = attrs.get('price')
        image = attrs.get('image')
        manufacturer_id = attrs.pop('manufacturer_id')

        errors = dict()

        try:
            attrs['manufacturer'] = CustomUser.objects.get(id=manufacturer_id)
        except ObjectDoesNotExist:
            errors['other'] = 'User Error: user was not found'

        return super().validate(attrs)

