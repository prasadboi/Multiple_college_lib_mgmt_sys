from library.models import Payment_bill, Seller_inventory
from django.urls import paths
from django.urls import render
from django.urls.conf import path 
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name = 'place_order'),
    path('enter_order_specs/', views.enter_order_specs,name='enter_order_specs'),
]