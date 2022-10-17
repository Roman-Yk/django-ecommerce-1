from email.message import EmailMessage
from django.shortcuts import render, redirect
from .forms import CustomerForm, CreateUserForm
from store.models import Customer

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
#to get user
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from store.decorators import unauthenticated_user

#import all for token
from django.http import HttpResponse  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.core.mail import EmailMessage  


# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else: 
            messages.info(request, "Username or password doesn't match")
    return render(request, 'users/login.html')

@unauthenticated_user  #e-commerce_with_js - Copy (2)
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            if User.objects.filter(email = form.cleaned_data.get('email')).exists():
                messages.warning(request, 'User with that email already exists')
                return redirect('register')
            else: 
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # to get the domain of the current site  
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('users/acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                    'token':account_activation_token.make_token(user),  
                })   
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject,message, to=[to_email]
                )
                email.send()
                #create customer instance
                customer,created = Customer.objects.get_or_create(
                    name = form.cleaned_data.get('username'),
                    email = form.cleaned_data.get('email'),
                    )
                if created:
                    customer.password = form.cleaned_data.get('password1'),               
                    customer.user = user
                else:
                    customer.password = form.cleaned_data.get('password1'),               
                    customer.user = user
                customer.save()
                
                #group attachment
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                
                username = form.cleaned_data.get('username')                
                messages.info(request, 'Please confirm your email address to complete the registration')
    else:
        form = CreateUserForm()           
    
    context = {'form': form}
    return render(request, 'users/register-page.html',context)

def logoutPage(request):
    logout(request)
    return redirect('store')
    
   
#account activation
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login into your account.')
        return redirect('login')
    else:
        return HttpResponse('activation link is invalid')