from rest_framework import serializers
from accounts.utils import get_user
from cars.models import Car
from legendarymotosports.utils import prepare_form_data
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    color = serializers.CharField(max_length=25)

    @staticmethod
    def get_data(request, car_pk=None) -> dict:
        user = get_user(request)
        data = prepare_form_data(request.data) # Contains chosen color from form
        data['car'] = car_pk # id of the car
        data['user'] = user.id # user id or None if user is Anonymous
        data['manufacturer'] = Car.objects.get(pk=car_pk).manufacturer.id
        return data
    
    
    def validate(self, attrs):
        color = attrs.get('color')

        errors = {}

        if not color:
            msg = 'Color was not chosen'
            errors['color'] = msg
        
        if errors:
            self.validation_errors = errors
            raise serializers.ValidationError()
        
        return super().validate(attrs)

