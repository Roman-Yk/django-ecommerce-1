from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logoutPage, name='logout'),
    
    #account activation
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name = 'activate' )
   
]
