from django.urls import path
from . import views 

urlpatterns = [
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('order-details/<int:orderId>/', views.order_details, name='order-details'),
    path('update-order-details/', views.update_order_details, name ='update_order_details')
]


