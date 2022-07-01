from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin,name='userlogin'),
     path('signup/', views.signup,name='signup'),
     path('home/', views.home ,name='home'),
     path('otp/', views.register_otp,name='otp'),
     path('forgotpassword/', views.forgotpassword,name='forgot'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword,name='resetp'),
    path('logout/', views.userlogout,name='userlogout'),
    path('userprofile/', views.userprofile,name='userprofile'),
    path('myorders/', views.myorders,name='myorders'),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    path('changepassword/', views.changepassword,name='changepassword'),
    path('order_detail/<int:order_id>/', views.order_detail,name='order_detail'),
     
]