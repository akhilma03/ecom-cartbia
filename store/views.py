
from pickle import GET
from django.shortcuts import get_object_or_404, render, redirect
from . models import Cartitems, Category, Filter_Price, Product, Sub_Category, Cart, Variation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


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
        if subcategory_slug != None:
            subcategories = get_object_or_404(
                Sub_Category, slug=subcategory_slug)
            products = Product.objects.filter(
                sub_category=subcategories, is_available=True)
            paginator = Paginator(products, 4)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            # subcategory_count= products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        filter_prices = Filter_Price.objects.all().order_by('id')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

        # if filter_prices:
        #     products =Product.objects.filter(filter_price=filter_prices)
        # else:
        #     products = Product.objects.all().filter(is_available = True).order_by('id')

    context = {
        'products': paged_products,
        'product_count': product_count,
        'subcategories': subcategories,
        'categories': categories,

    }
    return render(request, 'store/shop.html', context)


def product_details(request, category_slug, subcategory_slug, product_slug):
    try:
        print("my try")
        single_product = Product.objects.filter(
            category__slug=category_slug, sub_category__slug=subcategory_slug, slug=product_slug)
        related_products = Product.objects.filter(
            sub_category__slug=subcategory_slug)[0:4]

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'related_products': related_products,
    }
    return render(request, 'store/shop-details.html', context)


def filter_price(request):
    filter_prices = Filter_Price.objects.all().order_by('id')

    products = Product.objects.filter(filter_price=filter_prices)

    context = {
        'products': products,
    }

    return render(request, 'store/shop.html', context)


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
    if not cart:
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
                item.quantity += 1
                item.save()

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
                item.quantity += 1
                item.save()

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
                user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitems.objects.filter(cart=cart, is_active=True)
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
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = Cartitems.objects.filter(
                user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitems.objects.filter(cart=cart, is_active=True)
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
    return render(request, 'store/checkout.html', context)
