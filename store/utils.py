import json
from .models import *
from django.db.utils import IntegrityError
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print("cart", cart)
    except:
        cart = {}
        print("cart", cart)
    items= []
    order = {'get_cart_total': 0, 'get_cart_items':0, 'shipping': False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
                'product':{
                'id': product.id, 
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL,
                    },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
        
    return {'cartItems':cartItems, 'items': items, 'order':order}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
       cookieData = cookieCart(request)
       cartItems = cookieData['cartItems']
       order = cookieData['order']
       items = cookieData['items']
       customer = None
    return {'cartItems': cartItems, 'order': order, 'items': items, 'customer': customer}

def guestOrder(request, data):
    print('User is not logged in')
    print("COOKIES", request.COOKIES)
    
    name = data['form']['name']
    email = data['form']['email']
    existance = False
    cookieData = cookieCart(request)
    items = cookieData['items']
    #check if customer exists
    if Customer.objects.filter(email = email,name=name).exists():
        customer = Customer.objects.get(
            email = email,
            name=name,
        )
        existance = True
    #check if customer who esxisted wrote correct password and username
    elif Customer.objects.filter(email = email,name = name).exists() == False and (Customer.objects.filter(email=email).exists() or Customer.objects.filter(name=name).exists()):
        customer = False
        existance = False
    #check if customer with that credentials is'n exist, then create customer
    elif Customer.objects.filter(email = email,name=name).exists() == False and (Customer.objects.filter(email=email).exists() == False and Customer.objects.filter(name=name).exists() == False):
        customer = Customer.objects.create(email = email,name=name)
        existance = True
    
    if existance:
        order = Order.objects.create(
            customer=customer,
            completed = False,
        )
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            
            orderItem = OrderItem.objects.create(
                product= product,
                order = order,
                quantity = item['quantity'],
            )
    else:
        order = None
        
    return customer, order, existance