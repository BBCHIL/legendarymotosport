from django.urls import path

from search.views import CarSearchResultsView

urlpatterns = [
    path('', CarSearchResultsView.as_view(), name='car-search-init'), # for post request
    path('<str:search_word>/', CarSearchResultsView.as_view(), name='car-search'), # for get request
]