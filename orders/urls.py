from django.urls import path, include
from orders.views import MyOrderListView, OrderDetailView, OrderStatusViews

# These patterns are included in accounts.urls
urlpatterns = [
    path('orders/', MyOrderListView.as_view(), name='myorders'),
    path('orders/', include([
        path('<int:pk>/', OrderDetailView.as_view(), name='order-details'),
        path('delete/<int:pk>/', OrderDetailView.delete_order, name='order-delete'),
        path('status-next/<int:pk>/', OrderStatusViews.next_status, name='order-next-status'),
        path('status-previous/<int:pk>/', OrderStatusViews.previous_status, name='order-previous-status'),
    ]))
    
    
]
