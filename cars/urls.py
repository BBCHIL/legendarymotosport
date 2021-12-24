from django.urls import path
from django.urls.conf import include

from cars.views import (
    CarDetailView, CarEditView, CarListView, CarCreateView, 
)

urlpatterns = [
    path('cars/', CarListView.as_view(), name='cars'),
    path('cars/', include([
        path('search/', include('search.car_urls')),
        path('<int:pk>/', include('favorites.urls')),
        path('<int:pk>/', CarDetailView.as_view(), name='car-detail'),
        path('create/', CarCreateView.as_view(), name='car-create'),
        path('delete/<int:pk>/', CarDetailView.delete_car, name='car-delete'),
        path('edit/<int:pk>/', CarEditView.as_view(), name='car-edit'),
    ])),    
]
