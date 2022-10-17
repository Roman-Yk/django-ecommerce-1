from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UserInfo
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
import json
import datetime
from .utils import cartData, cookieCart, guestOrder
from django.contrib.auth.decorators import login_required

#import email settings
from django.core.mail import EmailMessage
from ecommerce import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth.tokens import default_token_generator as password_reset

#import pagination stuff
from django.core.paginator import Paginator


def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    
    products = Product.objects.all()
    categories = []
    for i in CATEGORY_CHOICES:
        categories.append(i[0])
        
    #Set up pagination
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
        
    context = {'products': products, 'cartItems': cartItems, 'order': order, 'choices': categories, 'items': items}
    return render(request, 'store/store.html', context)

def detail_view(request, productId):
    data = cartData(request)
    customer = data['customer']
    #get order to get access to cart items and ser orderitem
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    product = Product.objects.get(id=productId)
    #get order item to get access to the item quantity
    try:
        order_item = order.orderitem_set.get(product=product)
    except:
        order_item = {'quantity': 0}
    
    context={'product': product, 'order': order, 'orderitem': order_item}
    return render(request, 'store/detail-view.html', context)

@login_required(login_url='login')
def userProfile(request):
    data = cartData(request)
    customer = data['customer']
    user = request.user
    form = UserInfo(instance=customer)
    if request.method == "POST":
        form = UserInfo(request.POST, instance=customer)
        if form.is_valid():
            user.username = form.cleaned_data.get('name')
            user.email = form.cleaned_data.get('email')
            user.save()
            form.save()
            try:
                #get uploaded file 
                uploaded_file = request.FILES['document']
                #set uploaded file as avatar
                customer.avatar = uploaded_file
                customer.save()
            except:
                customer.avatar = customer.avatar
                customer.save()
            
            
    #get order instance to display items in cart
    order = data['order']
    context = {'form': form, 'order': order}
    return render(request, 'store/profile.html', context)

def cart(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    isEmpty = True
    if len(items) == 0:
        isEmpty = True
    else:
        isEmpty = False
    context = {'order':order, 'items':items, 'cartItems': cartItems, 'empty':isEmpty}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    exist = True
    customer = request.user.customer
    product = Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    #set item count variable
    quantity = orderItem.quantity
    
    if action == "add":
        orderItem.quantity += 1
        quantity += 1
    # Check if quantity is greater than 0 for avoid getting negative numbers
    if orderItem.quantity >= 1:
        if action == "remove":
            orderItem.quantity -= 1   
            quantity -=1
    
    orderItem.save()
    
    if orderItem.quantity <= 0 or action == "delete":
        orderItem.delete()
        exist = False
        quantity = 1

    
    return JsonResponse({
        'exist': exist,
        'itemQuantity': orderItem.quantity, 
        'quantity': quantity,
        'total': order.get_cart_total,
        'items': order.get_cart_items,
        'productPrice': orderItem.get_total,
        'singlePrice': orderItem.product.price
        }, 
        safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        existance = True
        
    else:
        customer, order, existance = guestOrder(request, data)
        
    if existance:
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
            
        if total == float(order.get_cart_total):
            order.completed = True
            
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order=order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
        #email configuration
        context={'name':customer.name,  'orderitems':order.orderitem_set.all(), 'order':order}
        template = render_to_string('store/email_template.html', context)
        email = EmailMessage(
            'You just placed an order.', 
            template,
            settings.EMAIL_HOST_USER,
            [customer.email]
        )
        email.fail_silently = False
        email.send()
        
    else:
        transaction_id = None
    
    return JsonResponse({'existance': existance, 'transactionId': transaction_id}, safe=False)


def reset_password_page(request):
    data = cartData(request)
    order = data['order']
    if request.method == 'POST':
        try:
            to_email = request.POST.get('email')
            user = User.objects.get(email=to_email)
            current_site = get_current_site(request)
            mesasage = render_to_string('store/reset_password/reset_pass_email.html', {
                'username': user.username,
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                'token':password_reset.make_token(user),  
            })
            mail_subject = 'Reset password'  
            email = EmailMessage(
                mail_subject,
                mesasage,
                to=[to_email]
            )
            email.send()
            messages.info(request, "Reset password link was sent to your email")
            return redirect('store')
        except User.DoesNotExist:
            messages.warning(request, "User with that email does not exists please register")
    context = {'order': order}
    return render(request, 'store/reset_password/reset_password_page.html', context)


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and password_reset.check_token(user,token):
        data = cartData(request)
        order = data['order']
        if request.method == 'POST':
            new_pass = request.POST.get('new_pass')
            pass_conf = request.POST.get('new_pass_conf')
            if new_pass == pass_conf:
                user.set_password(new_pass)
                user.save()
                customer = user.customer
                customer.password = new_pass
                customer.save()
                messages.success(request, "Password was successfully updated")
                return redirect('store')
            else:
                messages.warning(request, "Passwords doesn't match")  
        else:
            pass    
        return render(request, 'store/reset_password/reset_password.html', {'order':order})
    
    else:
        #return that user does not exsts page
        raise Http404
    
    



