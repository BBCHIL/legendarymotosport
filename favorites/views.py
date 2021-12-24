from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect

from rest_framework.views import APIView

from cars.models import Car

from accounts.utils import get_user
from favorites.models import Favorite

from favorites.serializers import FavoriteSerializer, LikeSerializer
from legendarymotosports.permissions import TokenPermission

class LikeView(APIView):
    serializer_class = LikeSerializer
    permission_classes = [TokenPermission, ]


    def get(self, request, pk):
        user = get_user(request)
        data = dict(
            user=user.pk, car=pk,
        )
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseBadRequest("Like validation failed")

        serializer.like(user, Car.objects.get(id=pk))
        return redirect('../../')


class CreateFavoriteView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [TokenPermission, ]

    def get(self, request, pk):
        user = get_user(request)
        data = dict(
            user=user.pk, car=pk,
        )
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseBadRequest("Favorite falidation failed")
        car = Car.objects.get(id=pk)
        try:
            Favorite.objects.get(user=user, car=car).delete()
        except ObjectDoesNotExist:
            Favorite.objects.create(user=user, car=car)
        return redirect('car-detail',pk=pk)

