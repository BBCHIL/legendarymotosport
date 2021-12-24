from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response

from cars.models import Car
from accounts.utils import get_user
from cars.serializers import CarSerializer
from legendarymotosports.utils import prepare_form_data


class CarSearchResultsView(APIView):
    template_name = 'cars/list.html'
    serializer_class = CarSerializer
 
    def get(self, request, search_word=None):
        
        user = get_user(request)
        cars = Car.objects.filter(name__icontains=search_word)
        self.serializer_class.prepare_render(cars, many=True, user=user)
        response_data = dict(
            user=user, cars=cars,
            include_search=True,
        )
        return Response(data=response_data)
    
    def post(self, request):
        """
        Redirects to get with needed data
        """
        data = prepare_form_data(request.data)
        print(request.data)
        print(data)
        
        return redirect('car-search', search_word=data.get('search'))


class CarFilterResultView(APIView):

    def get(self, request):
        pass

    def post(self, request):
        pass
