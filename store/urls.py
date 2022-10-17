from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path("detail-view/<int:productId>/", views.detail_view, name="detail_view"),
    
    path('profile/', views.userProfile, name='profile'),
    path('reset_password_page/', views.reset_password_page, name='reset_password_page'),
    path('reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', views.reset_password, name='reset_password'),
    
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    
]
