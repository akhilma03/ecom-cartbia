from email import message
from lib2to3.pgen2 import token
from multiprocessing import context
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render,redirect    
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,auth
from .forms import RegistrationForm
from django.contrib import messages
from . otp import *
from .models import Account

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def userlogin(request):
    if request.method == 'POST':
        email = request.POST ['email']
        password = request.POST ['password']
       
        user = authenticate(email=email,password=password)

        if user is not None:           
            login(request,user)
            # messages.success(request,'You are logged in')
            return redirect ('home')
        else:
            messages.error(request,'invalid credientail')   
            return redirect('userlogin') 

    return render(request,'accounts/userlogin.html')    

def signup(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            
            if Account.objects.filter(email=email).exists() :
                messages.error(request, 'Email already registered.')
            else :
                user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, mobile=mobile, password=password)
                user.save()
                request.session['mobile']=mobile
                send_otp(mobile)
            return redirect('otp')
    else:     
        form=RegistrationForm()
        context ={'form': form}

    return render(request,'accounts/signup.html',context)


    
def register_otp(request):
     if request.method == 'POST':
        check_otp = request.POST.get('otp')
        mobile=request.session['mobile']
        check=verify_otp(mobile,check_otp)
        if check:
            user = Account.objects.get(mobile = mobile)
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect('userlogin')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('otp')
     return render(request,'accounts/register_otp.html')
    #  return render(request,'accounts/register_otp.html')           

def home(request):
         return render(request,'accounts/home.html')     

def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            print('ok')
            user = Account.objects.get(email__exact=email)


            #reset password mail
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string ('accounts/reset_password.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Password reset mail have sent to your email')
            return redirect('userlogin')

        else:
            messages.error(request,'Account Not exist') 
            return redirect ('forgot')   

    return render(request,'accounts/forgotpassword.html')       

def resetpassword_validate(request,uidb64,token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']= uid
        messages.success(request,'Please reset your password')
        return redirect('resetp')
    else:
        messages.error(request,'This link has been expired')
        return redirect('userlogin')            


    # return HttpResponse('ok')

def resetpassword(request):
    if request.method == 'POST':
        create_password = request.POST['create_password']
        confirm_password = request.POST['confirm_password']

        if create_password == confirm_password:
             uid = request.session.get('uid')
             user = Account.objects.get(pk=uid)
             user.set_password(create_password)
             user.save()
             messages.success(request,'Password reset sucess')
             return redirect('userlogin')
           

        else:
            messages.error(request,'Password do not match!!!!')
            return redirect('resetp')
    else:      
        return render(request,'accounts/resetp.html')
