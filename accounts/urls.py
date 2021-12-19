from django.urls import path, include

from accounts.views import (
    AccountDeleteView, AccountEditView, BecomeManufacturerView, ButtonCodeActivationView, 
    FavoriteCarListView, FormCodeActivationView, HomePageView, 
    LoginView, LogoutView, RegistrationView, ResendActivationCodeView, UploadedCarsView, UsersOrdersView,
)

urlpatterns = [
    path('account/', HomePageView.as_view(), name='homepage'),
    path('account/', include('orders.urls')),
    path('account/', include([
        path('register/', RegistrationView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('activate/', FormCodeActivationView.as_view(), name='activate-by-form'),
        path('activate/<str:email>/', FormCodeActivationView.as_view(), name='activate-by-form'),
        path('activate/<str:email>/<str:activation_code>/', ButtonCodeActivationView.as_view(), name='activate-by-button'),
        path('resend/<str:email>/', ResendActivationCodeView.as_view(), name='resend-activation-code'),
        path('favorites/', FavoriteCarListView.as_view(), name='myfavorites'),
        path('edit/', AccountEditView.as_view(), name='account-edit'),
        path('join-us/', BecomeManufacturerView.as_view(), name='join-us'),
        path('uploaded/', UploadedCarsView.as_view(), name='car-uploads'),
        path('users-orders/', UsersOrdersView.as_view(), name='users-orders'),
        path('delete/', AccountDeleteView.as_view(), name='account-delete'),
    ])),
    
]

