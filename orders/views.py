from django.shortcuts import redirect, render
from store.views import Cartitems
from .forms import AddressForm
from .models import Address, Order
import datetime
from django.contrib import messages,auth

# Create your views here.
def placeOrder(request,total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0 , then redirect to shop
    cart_items = Cartitems.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (3 * total)/100
    grand_total = total + tax 
    print("addddiiiii")
    if request.method == 'POST':
        if 'address' in request.POST:
            address_id = request.POST['address']
            address = Address.objects.get(id=address_id)
            print("adddd")
            print(address)
        
            # Store all Billing information in Order Table
            data = Order()   # getting instance
            data.address = address
            data.user = current_user
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)

            data.order_number = order_number
            data.save()

            context={
                'tax':tax,
                'total':total,
                'cart_items':cart_items,
                'grand_total':grand_total,
                'address':address,
            }

            return render (request,'orders/payment.html', context)
        else:
            messages.error(request,'Please Enter a Address to Continue')
            return redirect('checkout')   
    else: 
        return redirect('checkout')                 

def payment(request):
    return render (request,'orders/payment.html',)