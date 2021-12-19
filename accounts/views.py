from re import X
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from cars.models import Car

from legendarymotosports.permissions import ManufacturerPermission, TokenPermission

from accounts.models import CustomUser
from accounts.serializers import (
    AccountEditSerializer, CodeActivationSerializer, LoginSerializer, 
    RegisterSerializer
)
from accounts.utils import get_user
from accounts.tasks import send_activation_code

from cars.serializers import CarSerializer
from favorites.models import Favorite

from legendarymotosports.utils import delete_files, prepare_form_data


class RegistrationView(APIView):
    template_name = 'accounts/registration.html'

    def get(self, request):
        user= get_user(request)
        response_data = dict(
            user=user,
        )
        return Response(data=response_data)
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            user = get_user(request)
            response_data = dict(
                errors=serializer.validation_errors,
                user=user,
            )
            return Response(response_data)
        
        user = CustomUser.objects.create_user(
            **serializer.validated_data
        )
        send_activation_code(user.email, user.activation_code)
        return redirect('activate-by-form', user.email)


class LoginView(APIView):
    template_name = 'accounts/login.html'
    serializer_class = LoginSerializer

    def get(self, request):
        user = get_user(request)
        response_data = dict(
            user=user,
        )
        return Response(data=response_data)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            user = get_user(request)
            response_data = dict(
                errors=serializer.validation_errors,
                user=user,
            )
            return Response(response_data)

        token, created = Token.objects.get_or_create(
            user=serializer.validated_data.get('user')
        )

        response = redirect('homepage')
        response.set_cookie('auth_token', token)

        return response


class LogoutView(APIView):
    def get(self, request):
        response = redirect('login')
        response.delete_cookie('auth_token')
        return response


class HomePageView(APIView):
    template_name = 'accounts/home.html'
    def get(self, request):
        user = get_user(request)
        # img = user.get('image')
        return Response({'user': user})


class ButtonCodeActivationView(APIView):

    serializer_class = CodeActivationSerializer
    template_name = 'accounts/email.html'

    def get(self, request, email=None, activation_code=None):
        if email and activation_code:
            serializer_data = dict(
                email=email, 
                activation_code=activation_code,
            )
            serializer = self.serializer_class(data=serializer_data)
            if not serializer.is_valid():
                return HttpResponseBadRequest("Validation Failed")

            user = CustomUser.objects.get(
                email=serializer.validated_data['email'],
            )
            serializer.set_active(user)
            return redirect('login')


class FormCodeActivationView(APIView):

    serializer_class = CodeActivationSerializer
    template_name = 'accounts/activation.html'

    def get(self, request, email=None):
        user = get_user(request)
        response_data = dict(
            email=email, user=user
        )
        return Response(data=response_data)

    def post(self, request, email=None):
        
        serializer_data = prepare_form_data(request.data)
        if email: # If email not in url it comes from serializer
            serializer_data['email'] = email
        serializer = self.serializer_class(data=serializer_data)
        if not serializer.is_valid():
            user = get_user(request)
            response_data = dict(
                email=email, user=user,
                errors=serializer.validation_errors
            )
            return Response(data=response_data)
        user = CustomUser.objects.get(
            email=serializer.validated_data.get('email')
        )
        serializer.set_active(user)
        return redirect('login')
            

class ResendActivationCodeView(APIView):

    def get(self, request, email=None):
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("User does not exists")
        send_activation_code(user.email, user.activation_code)
        return redirect('activate-by-form', email=user.email)


class FavoriteCarListView(APIView):
    template_name = 'cars/list.html'
    serializer_class = CarSerializer

    def get(self, request):
        user = get_user(request)
        favs = Favorite.objects.filter(user=user)
        cars = self.serializer_class.get_from_favorites(favs)
        self.serializer_class.prepare_render(cars, many=True, user=user)
        response_data = dict(
            user=user, cars=cars,
        )
        return Response(data=response_data)


class AccountEditView(APIView):
    serializer_class = AccountEditSerializer
    template_name = 'accounts/edit.html'
    permission_classes = [TokenPermission, ]

    def get(self, request):
        user = get_user(request)
        response_data = dict(
            user=user,
        )
        return Response(data=response_data)
    

    def post(self, request):
        user = get_user(request)
        data = self.serializer_class.get_data(request) 
        serializer = self.serializer_class(data=data)
        
        if not serializer.is_valid():
            response_data = dict(
                errors=serializer.validation_errors,
                user=user,
            )
            return Response(data=response_data)

        serializer.put_changes(user, serializer.validated_data)
        return redirect('homepage')


class AccountDeleteView(APIView):

    def get(self, request):
        from django.contrib.auth.models import AnonymousUser
        user = get_user(request)
        if isinstance(user, AnonymousUser):
            return HttpResponseBadRequest('You are not even logged in')
        delete_files(user)
        user.delete()
        response = redirect('homepage')
        response.delete_cookie('auth_token')
        return response


class BecomeManufacturerView(APIView):
    """
    User push button -> Email sents to admin -> 
    Admin decide to accept or decline the request ->
    Response sent to user Email.
    """
    permission_classes = [TokenPermission, ]
    def get(self, request):
        user = get_user(request)
        # user.manufacturer_code = get_random_string(length=10)
        # send_manufacturer_confirm(user.email, user.manufacturer_code)
        user.is_manufacturer = True
        user.save()
        return redirect('homepage')


class UploadedCarsView(APIView):
    permission_classes = [TokenPermission, ManufacturerPermission, ]
    serializer_class = CarSerializer
    template_name = 'cars/list.html'

    def get(self, request):
        user = get_user(request)
        cars = Car.objects.filter(manufacturer=user)
        self.serializer_class.prepare_render(cars, many=True)
        response_data = dict(
            cars=cars, user=user,
        )
        return Response(data=response_data)


class UsersOrdersView(APIView):
    permission_classes = [TokenPermission, ManufacturerPermission, ]
    template_name = 'orders/list.html'

    def get(self, request):
        user = get_user(request)
        orders = user.user_orders.all()
        response_data = dict(
            user=user, orders=orders,
        )
        return Response(data=response_data)