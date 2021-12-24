from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import views
from rest_framework.decorators import api_view

from accounts.utils import get_user


from rest_framework.views import APIView
from rest_framework.response import Response

from cars.serializers import CarCreateSerializer, CarEditSerializer, CarSerializer
from cars.models import Car
from legendarymotosports.utils import delete_files

from orders.models import Order

from legendarymotosports.permissions import ManufacturerPermission, TokenPermission
from orders.serializers import OrderSerializer


class CarListView(APIView):
    template_name = 'cars/list.html'
    serializer_class = CarSerializer

    def get(self, request):
        cars = Car.objects.all()
        user = get_user(request)
        self.serializer_class.prepare_render(cars, many=True, user=user)
        response_data = dict(
            cars=cars, user=user,
            include_search=True,
        )
        return Response(data=response_data)


class CarDetailView(APIView):
    """
    GET shows car page, post to make order.
    """
    template_name = 'cars/details.html'
    serializer_class = CarSerializer

    def get(self, request, pk):
        user = get_user(request)
        car = Car.objects.get(id=pk)
        self.serializer_class.prepare_render(car, user=user)
        response_data = dict(
            car=car, user=user,
        )
        return Response(data=response_data)

    def post(self, request, pk):
        # request.data only contains color, other data is getting from here
        data = OrderSerializer.get_data(request, car_pk=pk) 
        serializer = OrderSerializer(data=data)

        if not serializer.is_valid():
            return HttpResponse('Validation Failed')
        Order.objects.create(
            **serializer.validated_data
        )
        return redirect('myorders')
    
    @api_view(['GET'])
    def delete_car(request, pk):
        user = get_user(request)
        try:
            car = Car.objects.get(id=pk, manufacturer=user)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Car does not exists or You have no permission to delete it')
        else:
            delete_files(car)
            car.delete()
            return redirect('car-uploads')

    

class CarCreateView(views.APIView):
    template_name = 'cars/create.html'
    serializer_class = CarCreateSerializer
    permission_classes = [TokenPermission, ManufacturerPermission, ]


    def get(self, request):
        user = get_user(request)
        response_data = dict(
            user=user,
        )
        return Response(data=response_data)
    
    def post(self, request):
        serializer_data = self.serializer_class.get_data(request)
        serializer = self.serializer_class(data=serializer_data)
        
        if not serializer.is_valid():
            return Response(errors=serializer.validation_errors)
        
        Car.objects.create(
            **serializer.validated_data
        )
        return redirect('car-uploads')


class CarEditView(APIView):
    template_name = 'cars/edit.html'
    serializer_class = CarEditSerializer

    def get(self, request, pk):
        user = get_user(request)
        response_data = dict(
            user=user,
        )
        return Response(data=response_data)
    

    def post(self, request, pk):
        user = get_user(request)
        data = self.serializer_class.get_data(request)
        serializer = self.serializer_class(data=data)
        response_data = dict(
            user=user,
        )
        if not serializer.is_valid():
            response_data['errors'] = serializer.validation_errors
            return Response(data=response_data)
        
        car = Car.objects.get(pk=pk)
        
        self.serializer_class.put_changes(car, serializer.validated_data)

        return redirect('car-detail', pk=pk)

