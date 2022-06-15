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
     
]