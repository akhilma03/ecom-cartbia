from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.adminlogin,name='adminlogin'),
    path('home/', views.adminhome,name='dashboard'),
    path('productz/', views.product,name='product'),
    path('addproduct/', views.addproduct,name='addproduct'),
     
] + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)