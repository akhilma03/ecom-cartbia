from django.shortcuts import get_object_or_404, render, redirect
from . models import Cartitems, Category, Product, Sub_Category, Cart, Variation,wishlist,ReviewRating,Filter_Price
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import Address
from orders.forms import AddressForm
from django.contrib import messages
from orders.models import Discount,Discount_coupon,OrderProduct
from .forms import ReviewForm


def homei(request):
    products = Product.objects.all().filter(
        is_available=True).order_by('-id')[0:8]

    context = {
        'products': products
    }
    return render(request, 'store/index.html', context)


def shop(request, category_slug=None, subcategory_slug=None):
    categories = None
    products = None
    subcategories = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if 'sorting' in request.POST:
            if request.method == 'POST':
                    sort_id = request.POST['sorting']

                    if sort_id == 'low':
                        product = Product.objects.filter(category=categories).order_by('price')
                        count = product.count()
                        paginator = Paginator(product,4)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)

                    else:
                        product = Product.objects.filter(category=categories).order_by('-price')
                        count = product.count()
                        paginator = Paginator(product,4)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)


         #
        if 'sorting' not in request.POST: 
            if request.method =='POST':
                print('212222222')
                sort = request.POST['filtering']
                key = Filter_Price.objects.get(name = sort)
                a = key.pricerange_from
                b = key.pricerange_to
                products= Product.objects.filter(category=categories,price__range=(a,b))
                paginator = Paginator(products, 4)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)


        if subcategory_slug != None:
            subcategories = get_object_or_404(
                Sub_Category, slug=subcategory_slug)
            products = Product.objects.filter(
                sub_category=subcategories, is_available=True)
            paginator = Paginator(products, 4)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            # subcategory_count= products.count()
            if 'filtering'  not in request.POST: 
                if request.method =='POST':
                    sort_id = request.POST['sorting']

                    if sort_id == 'low':
                        product = Product.objects.filter(sub_category=subcategories).order_by('price')
                        count = product.count()
                        paginator = Paginator(product,4)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)

                    else:
                        product = Product.objects.filter(sub_category=subcategories).order_by('-price')
                        count = product.count()
                        paginator = Paginator(product,4)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)

            if 'filtering'  in request.POST: 
                if request.method == 'POST':
                    sort = request.POST['filtering']
                    key = Filter_Price.objects.get(name=sort)
                    a = key.pricerange_from
                    b = key.pricerange_to
                    product= Product.objects.filter(sub_category=subcategories,price__range=(a,b))
                    paginator = Paginator(product, 4)
                    page = request.GET.get('page')
                    paged_products = paginator.get_page(page)        


    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

        if 'filtering' in request.POST:
            if request.method == 'POST':
                
                sort =request.POST['filtering']
                key = Filter_Price.objects.get(name=sort)
                a = key.pricerange_from
                b=key.pricerange_to
                print(b)
                product= Product.objects.filter(price__range=(a,b))
                print(product)
                paginator = Paginator(product, 4)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)    


        if 'filtering' not in request.POST:
            if request.method == 'POST':
                    sort_id = request.POST['sorting']
                    
                    if sort_id == 'low':
                        products = Product.objects.all().filter(is_available=True).order_by('price')
                        count = products.count()
                        paginator = Paginator(products,6)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)

                    else:
                        products = Product.objects.all().filter(is_available=True).order_by('-price')
                        count = products.count()
                        paginator = Paginator(products,6)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)

    filter = Filter_Price.objects.all().order_by('id')
    context = {
        'products': paged_products,
        'product_count': product_count,
        'subcategories': subcategories,
        'categories': categories,
        'filter':filter,

    }
    return render(request, 'store/shop.html', context)


def product_details(request, category_slug, subcategory_slug, product_slug):
    try:
        print("my try")
        single_product = Product.objects.get(
            category__slug=category_slug, sub_category__slug=subcategory_slug, slug=product_slug)
        related_products = Product.objects.filter(
            sub_category__slug=subcategory_slug)[0:4]

    except Exception as e:
        raise e
    if request.user.is_authenticated:   
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id = single_product.id ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None    
    else:
        orderproduct = None 
    reviews = ReviewRating.objects.filter(product_id = single_product.id ,status = True)     
    context = {
        'single_product': single_product,
        'related_products': related_products,
        'orderproduct':orderproduct,
        'reviews':reviews,
        
    }
    return render(request, 'store/shop-details.html', context)




def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            
            products = Product.objects.order_by('-id').filter(Q(description__icontains=keyword) | Q(
                product_name__icontains=keyword) | Q(category__category_name__icontains=keyword))
            product_count = products.count()
        else:
            return redirect('shop')

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/shop.html', context)

# getting session id
# sessionkey is session id


def _cart_id(request):

    cart = request.session.session_key
    if not cart: # if no session create new one
        cart = request.session.create()
    return cart


def addcart(request, product_id):
    current_user = request.user
    # get the product  #getting session in cart   using cartid
    product = Product.objects.get(id=product_id)

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                print(key)
                print(value)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = Cartitems.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = Cartitems.objects.filter(
                product=product, user=current_user)
            # is the current variation inside the existing variations then increse qnty cart item
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # increase cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = Cartitems.objects.get(product=product, id=item_id)
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')    


            else:
                item = Cartitems.objects.create(
                    product=product, quantity=1, user=current_user)
                # create new cart item
                # checking product variation empty or not
                if len(product_variation) > 0:
                    item.variations.clear()
                    # cart_item.quantity += 1    # incresing quantinty in cart
                    item.variations.add(*product_variation)
                    print(item)
                    item.save()
        # except Cartitems.DoesNotExist:
        else:
            cart_item = Cartitems.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

     # if user is not authenticated
    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                print(key)
                print(value)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            # get cart using cart id present in session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
            # putting product inside cart
        is_cart_item_exists = Cartitems.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = Cartitems.objects.filter(product=product, cart=cart)
            # existing variations
            # current variations
            # item_id

            # is the current variation inside the existing variations then increse qnty cart item
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in existing_variation_list:
                # increase cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = Cartitems.objects.get(product=product, id=item_id)
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')    

            else:
                item = Cartitems.objects.create(
                    product=product, quantity=1, cart=cart)
                # create new cart item
                # checking product variation empty or not
                if len(product_variation) > 0:
                    item.variations.clear()
                    # cart_item.quantity += 1    # incresing quantinty in cart
                    item.variations.add(*product_variation)
                    print(item)
                    item.save()
        # except Cartitems.DoesNotExist:
        else:
            cart_item = Cartitems.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitems.objects.get(product=product, user=request.user, id=cart_item_id)
        else:  
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitems.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_items(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)


    if request.user.is_authenticated:
         cart_item = Cartitems.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitems.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitems.objects.filter(
                user=request.user, is_active=True).order_by('-id')

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitems.objects.filter(cart=cart, is_active=True).order_by('-id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            print(total)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }

    return render(request, 'store/shopping-cart.html', context)


@login_required(login_url='userlogin')
def checkout(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax = 0
        grand_total = 0
        address = None
        start = 0
        discount=0
        discount_price=0
        data=0
      
            
        if request.method == 'POST':
            form = AddressForm(request.POST)    
            if form.is_valid():
                print("valid")
                # Store all Billing information in Order Table
                data = Address()   # getting instance
                data.user= request.user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line1 = form.cleaned_data['address_line1']
                data.address_line2 = form.cleaned_data['address_line2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.district = form.cleaned_data['district']
                data.city = form.cleaned_data['city']
                data.pincode = form.cleaned_data['pincode']   
                data.save() 
                return redirect('checkout')
            else:
                print("bnotvalid")

        
        cart_items = Cartitems.objects.filter(user=request.user, is_active=True)
        address = Address.objects.filter(user=request.user)
        coppen = Discount.objects.all()
       
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            print(total)
            quantity += cart_item.quantity

        
        if request.method=='POST':
            checkd = Discount_coupon.objects.filter(user=request.user).exists()
            if checkd:
                Discount_coupon.objects.filter(user=request.user).delete()
            
            try:
                coupon = request.POST['coupon']
                # check = Discount.objects.filter(code=coupon)
                checked = Discount.objects.get(code=coupon)
                if checked:
                    start =checked.discount_from
                    discount = checked.discount_percentage
                else:
                        pass   
            except:
                tax = (1 * total)/100
                grand_total = total + tax
            
        else:
            tax = (1 * total)/100
            grand_total = total + tax


        print(start)
        print(discount)
                  
        tax = (1 * total)/100
        grand_total_without = total + tax 
        print(quantity)
        try:
            if start:
                if grand_total_without >= start:
                    discount_price = int(grand_total_without * discount / 100)
                    grand_total =int(grand_total_without - discount_price)
                    data = Discount_coupon()
                    data.user = request.user
                    data.discount_applied=discount_price
                    data.save()
        except:
            grand_total = int(grand_total_without)
     
        
        
    except ObjectDoesNotExist:
        pass



    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'discount_price':discount_price,
        'address':address, 
        'data':data,
        'coppen':coppen

    }
    return render(request, 'store/checkout.html', context)

def contact(request):
    return render(request,'store/contact.html')

def Wishlist(request):
    wlist = wishlist.objects.filter(user=request.user)

    context = {
        'wlist':wlist
    }
    return render(request,'store/wishlist.html',context)


def addwish(request,id):
    product = Product.objects.get(id=id)

    check  = wishlist.objects.filter(product=product).exists()

    if not check:
        wish = wishlist()
        wish.user = request.user
        wish.product = product
        wish.save()
    return redirect ('shop')

def removewish(request,id):
    wish = wishlist.objects.get(id=id)
    wish.delete()
    return redirect ('wishlist')    


def submit_review(request,product_id):
    print('hg')
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        print('hli')
        try:
            print('hello')
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            forms = ReviewForm(request.POST,request.FILES,instance=reviews,)
            forms.save()
            messages.success(request,'Your Review has been updated')
            return redirect(url)


        except ReviewRating.DoesNotExist: 
            print('haiiiiii')
            form = ReviewForm(request.POST,request.FILES)
            print('ghds')
            if form.is_valid():
                print('ghlkds')
                data = ReviewRating() 
                data.subjects = form.cleaned_data['subjects']
                print(data.subjects)
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id 
                data.save()
                messages.success(request,'Thank You For Your Review')
                return redirect(url)