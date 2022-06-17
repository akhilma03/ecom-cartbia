import razorpay
from django.shortcuts import redirect, render
from store.views import Cartitems,Product
from .forms import AddressForm
from .models import Address, Order, OrderProduct, Payment
import datetime
from django.contrib import messages,auth
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


from http import client

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
    print("hello")
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
            request.session['order_number']=order_number

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

    current_user = request.user
    cart_items = Cartitems.objects.filter(user=current_user)
    grand_total = 0
    total= 0
    tax = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (3 * total)/100
    grand_total = (total + tax)*100 
    paisa = grand_total/100
 

#create razor pay client

    Client =razorpay.Client(auth=('rzp_test_jiqUdEu9mZHhRH','dCivm5cm9vpJ4flAeFzB001J'))
    #create order

    response_payment=Client.order.create(dict( amount=grand_total,currency='INR'))

    order_id = response_payment['id']
    order_status = response_payment['status']
    total += (cart_item.product.price * cart_item.quantity)
    if order_status == 'created':
        pay = Payment()
        pay.user = current_user
        pay.amount_paid = grand_total
        pay.order_id = order_id
        pay.save()


       
    context= {
        'payment':response_payment,
        'grand_total':paisa,
        'tax':tax,
        'total':total,
    }    

    return render (request,'orders/razorpayment.html',context)

def payment_status(request):
    print('annnaa')
    response = request.POST
    print(response)
    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }
    #client instance

    client = razorpay.Client(auth=('rzp_test_jiqUdEu9mZHhRH','dCivm5cm9vpJ4flAeFzB001J'))
    try:
        status =client.utility.verify_payment_signature(params_dict)
        payment=Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id=response['razorpay_payment_id'] 
        payment.paid=True 
        payment.save() 
        
        print(payment)
        print("kjhkj")

        order_number=request.session['order_number'] 
        print(order_number) 
        order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number) 
        order.payment=payment  
        order.status='Completed' 
        order.is_ordered = True
        order.save()

    #  # Move the cart item into order product table
        cart_items = Cartitems.objects.filter(user=request.user)
        print('hello')

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id =request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price= item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # take cartitem by cart for the getting variation   

            cart_item = Cartitems.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id) # geting order product id from after saving 
            orderproduct.variations.set(product_variation)
            orderproduct.save()

    #     #Reduced the quantity

            product= Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

         
    #     # clear cart
        Cartitems.objects.filter(user=request.user).delete()

    #     #Send Order recieved email to customer

        mail_subject = 'Thank You For Shopping with us  '
        message = render_to_string('orders/order_recieved.html', {
            'user': request.user,
            'order':order,
            
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()



        return render(request,'orders/payments_status.html',{'status':True})
    except:    
        return render(request,'orders/payments_status.html',{'status':False})    