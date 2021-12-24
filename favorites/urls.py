from django.urls import path
from favorites.views import CreateFavoriteView, LikeView

# Included in cars.urls
urlpatterns = [
    path('like/', LikeView.as_view(), name='like'),
    path('favorite/', CreateFavoriteView.as_view(), name='favorite'),
]

