from django.shortcuts import render
from store.decorators import allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from store.models import *
from django.http import JsonResponse
import json
# Create your views here.

@admin_only
def admin_panel(request):
    orders = Order.objects.filter(completed=True).order_by("sended", '-date_ordered')
    context = {'orders': orders}
    for order in orders:
        try:
            address = ShippingAddress.objects.get(order=order)
        except:
            order.sended = True
            order.save()
    return render(request, 'panel/admin_panel.html', context)

@admin_only
def order_details(request, orderId):
    order = Order.objects.get(id=orderId)
    orderItems = order.orderitem_set.all()
    try:
        address = ShippingAddress.objects.get(order=order)
    except:
        order.sended = True
        order.save()
        address = None
    context = {'order':order, 'orderItems': orderItems, 'address':address}
    return render(request, 'panel/order-details.html', context)

def update_order_details(request):
    data = json.loads(request.body)
    order = Order.objects.get(id=int(data['order']))
    order.sended = data['sended']
    order.save()
    return JsonResponse({'sended': order.sended}, safe=False)
