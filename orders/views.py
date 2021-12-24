
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view

from legendarymotosports.permissions import TokenPermission

from orders.models import Order

from accounts.utils import get_user

# Order objects creates in cars.views.CarDetailView

class MyOrderListView(views.APIView):
    template_name = 'orders/list.html'
    def get(self,request):
        user = get_user(request)
        myorders = Order.objects.filter(user=user)
        response_data = dict(
            user=user, orders=myorders,
        )
        return Response(data=response_data)


class OrderDetailView(views.APIView):
    """
    Users able to confirm if order arrived,
    manufacturers can change order status and delete it
    """
    template_name = 'orders/details.html'
    permission_classes = [TokenPermission, ]

    def get(self, request, pk):
        user = get_user(request)
        order = Order.objects.get(id=pk)
        user.is_owner = bool(order.manufacturer.id == user.id)
        user.is_ordered_by = bool(order.user.id == user.id)
        response_data = dict(
            user=user,
            order=order,
        )
        if user.is_owner:
            msg = (
                # 'You can change order status by pressing buttons below \n'
                'Possible statuses: {}\n'
                'Current status: {}\n'.format(
                    '->'.join(i[0] for i in order.STATUS),
                    order.status,
                )    
            )
            response_data['text_info'] = msg
        
        if user.is_owner or user.is_ordered_by:
            return Response(data=response_data)
        return HttpResponseForbidden('Permission denied')

    @api_view(['GET'])
    def delete_order(request, pk):
        user = get_user(request)
        order = Order.objects.get(id=pk)
        if not order.user.id == user.id:
            return HttpResponseBadRequest('You have no permission to delete this order')
        order.delete()
        return redirect('myorders')


class OrderStatusViews:
    """
    This class is different, it just contains some methods that 
    has similar functions, but i dont want to create another class for 
    each of them.
    """
    status_table = dict(enumerate((i[0] for i in Order.STATUS))) # To get status by index
    reversed_table = {v:k for k, v in status_table.items()} # To get index by status

    @api_view(['GET'])
    def next_status(request,  pk):
        user = get_user(request)
        order = Order.objects.get(id=pk)

        index = OrderStatusViews.reversed_table[order.status] # Current status index
        
        if order.manufacturer.id == user.id:
            if index == max(OrderStatusViews.status_table):
                return HttpResponseBadRequest('This is the last possible status')
            else:
                order.status = OrderStatusViews.status_table[index+1] # Changing status
                order.save()
                return redirect('order-details', pk=order.id)
        else:
            return HttpResponseBadRequest('You are not allowed to change status of this order')
            

    @api_view(['GET'])
    def previous_status(request, pk):

        user = get_user(request)
        order = Order.objects.get(id=pk)

        index = OrderStatusViews.reversed_table[order.status] # Current status index
        
        if order.manufacturer.id == user.id:
            if index == min(OrderStatusViews.status_table):
                return HttpResponseBadRequest('This is the first possible status')
            else:
                order.status = OrderStatusViews.status_table[index-1]
                order.save()
                return redirect('order-details', pk=order.id)
        else:
            return HttpResponseBadRequest('You are not allowed to change status of this order')
    


        

                
