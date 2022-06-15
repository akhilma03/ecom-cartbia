
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.contrib import messages,auth
from . otp import *
from .models import Account
from store.views import _cart_id
from store.models import Cart, Cartitems
import requests


# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = Cartitems.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    print("yes")
                    cart_item = Cartitems.objects.filter(cart=cart)
                    #getting the product variations by cart id 
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cartitems from the user to acess to his product variations

                    cart_item = Cartitems.objects.filter( user=user)
            # is the current variation inside the existing variations then increse qnty cart item
                    existing_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id) 

                        #product vartion [1,2,3,4]
                        # ext vartion [2,3,5,6,] the both same value we want to combine
                          
                    for pr in product_variation:
                        if pr in existing_variation_list:
                            index = existing_variation_list.index(pr)
                            item_id = id[index]
                            item = Cartitems.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save() 
                        else:
                            cart_item = Cartitems.objects.filter(cart=cart)    
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                print('Entering except')
                pass

            auth.login(request, user)
            # messages.success(request,'You are logged in')
            url = request.META.get('HTTP_REFERER')   # getting previous url for checkout login
            try:
                query = requests.utils.urlparse(url).query
                # next =/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                    
            except:
                return redirect('home')
        else:
            messages.error(request, 'invalid credientail')
            return redirect('userlogin')

    return render(request, 'accounts/userlogin.html')


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

            if Account.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = Account.objects.create_user(
                    first_name=first_name, last_name=last_name, email=email, mobile=mobile, password=password)
                user.save()
                request.session['mobile'] = mobile
                send_otp(mobile)
            return redirect('otp')
    else:
        form = RegistrationForm()
        context = {'form': form}

    return render(request, 'accounts/signup.html', context)


def register_otp(request):
    if request.method == 'POST':
        check_otp = request.POST.get('otp')
        mobile = request.session['mobile']
        check = verify_otp(mobile, check_otp)
        if check:
            user = Account.objects.get(mobile=mobile)
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect('userlogin')
        else:
            messages.info(request, 'Invalid OTP')
            return redirect('otp')
    return render(request, 'accounts/register_otp.html')
    #  return render(request,'accounts/register_otp.html')


def home(request):
    return render(request, 'accounts/home.html')


def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            print('ok')
            user = Account.objects.get(email__exact=email)

            # reset password mail
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Password reset mail have sent to your email')
            return redirect('userlogin')

        else:
            messages.error(request, 'Account Not exist')
            return redirect('forgot')

    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetp')
    else:
        messages.error(request, 'This link has been expired')
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
            messages.success(request, 'Password reset sucess')
            return redirect('userlogin')

        else:
            messages.error(request, 'Password do not match!!!!')
            return redirect('resetp')
    else:
        return render(request, 'accounts/resetp.html')


def userlogout(request):
    logout(request)
    return redirect('home')
