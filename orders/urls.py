from django.urls import path
from . import views

urlpatterns = [
    path('', views.placeOrder,name='place_order'),
    path('payments/', views.payment,name='payment'),

     
]