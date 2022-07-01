
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from store.models import Product, Variation, Category, Sub_Category,Filter_Price
from django.db.models.functions import ExtractMonth
from django.db.models import  Count
from orders.models import OrderProduct, Order,Discount
from accounts.models import Account
from.forms import BannerForm, ProductForm, CategoryForm, Sub_CategoryForm, VariationForm, OrderForm,DiscountForm,AccountForm,FilterForm
from accounts.otp import *
from . models import Banners
import calendar
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator




a= Account.objects.filter(is_superadmin= True)



# Create your views here.
def adminlogin(request):
      if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_superadmin:
                login(request, user)
                # messages.success(request,'You are logged in')
                return redirect('dashboard')
        else:
            messages.error(request, 'invalid credientail')
            return redirect('adminlogin')

      return render(request, 'adminz/adminlogin.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')


@user_passes_test(lambda u: u in a, login_url='adminlogin')
def adminhome(request):
    orders = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
   #order 
    order_delivered = Order.objects.filter(status='Delivered')
    order_shipped   = Order.objects.filter(status='shipped')
    order_cancelled = Order.objects.filter(status='ordered')
    orders = Order.objects.all()
    number_orders = orders.count()
    odata = [
        order_delivered.count(),
        order_shipped.count(),
        order_cancelled.count(),
        ]
    olabel = ['Deliverd','Shipped','Ordered']
#user
    user =Account.objects.filter(is_superadmin = False) 
    ucount = user.count()
    orderp = OrderProduct.objects.all().order_by('-id')[:6]
    total_products = Product.objects.all().count()
    total_orders = Order.objects.all().count()
    total_cat = Category.objects.all().count()


#Revenew
# total revenue in rupee
    total_revenue = 0
    orders_withoutcancel = Order.objects.exclude(status='Cancelled')
    for order in orders_withoutcancel:
        total_revenue += int(order.order_total)

    context = {
        'monthNumber':monthNumber,
        'totalOrders':totalOrders,
         'total_products':total_products,
        'total_orders':total_orders,
        'ucount':ucount,
        'orderp':orderp,
        'total_cat':total_cat,
         'number_orders': number_orders ,
        'odata': odata ,
        'olabel': olabel ,
        'total_revenue':total_revenue
    }
    return render(request, 'adminz/dashboard.html',context)







# @user_passes_test(lambda u: u in a,login_url='adminlogin')
@user_passes_test(lambda u: u in a, login_url='adminlogin')
def product(request):

    products = Product.objects.all().filter(is_available=True).order_by('-id')
    paginator =  Paginator(products,8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)



    context = {

       'products': paged_products,
        }

    return render(request, 'adminz/products.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addproduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.error(request, 'invalid input')
            return redirect('addproduct')

    else:
        form = ProductForm()

    context = {

       'form': form,

    }
    return render(request, 'adminz/addproduct.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def category(request):

    categories = Category.objects.all().order_by('-id')

    
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                categories=Category.objects.filter(Q(category_name__icontains=keyword))

    context = {
        'categories': categories
    }
    return render(request, 'adminz/category.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def subcategory(request):

    subcategories = Sub_Category.objects.all().order_by('-id')
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                subcategories=Sub_Category.objects.filter(Q(sub_categoryname__icontains=keyword))

    context = {
        'subcategories': subcategories
    }
    return render(request, 'adminz/subcategory.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addcategory(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')

    else:
        form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'adminz/add_category.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def edit_category(request, slug):

    categories = Category.objects.get(slug=slug)
    form = CategoryForm(instance=categories,)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=categories)
        if form.is_valid():
            form.save()
            return redirect('category')

    context = {
        'form': form
    }
    return render(request, 'adminz/edit_category.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addsubcategory(request):
    form = Sub_CategoryForm()

    if request.method == 'POST':
        form = Sub_CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory')

    else:
        form = Sub_CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'adminz/add_subcategory.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def editS(request, slug):
    subcat = Sub_Category.objects.get(slug=slug)
    form = Sub_CategoryForm(instance=subcat,)
    if request.method == 'POST':
        form = Sub_CategoryForm(request.POST, request.FILES, instance=subcat)
        if form.is_valid():
            form.save()
            return redirect('subcategory')

    context = {
        'form': form,
    }

    return render(request, 'adminz/hello.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Deletecategory(request, slug):
     categories = Category.objects.get(slug=slug)
     categories.delete()
     return redirect('category')

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Deletesubcategory(request, slug):
     subcategories = Sub_Category.objects.get(slug=slug)
     subcategories.delete()
     return redirect('subcategory')

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def edit_products(request, id):
    products = Product.objects.get(id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=products)

        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.error(request, 'invalid input')

    form = ProductForm(instance=products)
    context = {

       'form': form,

    }
    return render(request, 'adminz/editProduct.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def productsdetails(request):

    products = Product.objects.all().filter(is_available=True).order_by('-id')

    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                products=Product.objects.filter(Q(product_name__icontains=keyword))

    paginator =  Paginator(products,8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {

       'products': paged_products,


    }

    return render(request, 'adminz/tablepro.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def deleteproduct(request, id):
     products = Product.objects.get(id=id)
     products.delete()
     return redirect('productdetails')

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def variationz(request):
    variations = Variation.objects.all().order_by('-id')

    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                variations=Variation.objects.filter(Q(product__product_name__icontains=keyword))

    context = {
        'variations': variations
    }
    return render(request, 'adminz/variation.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addvariationz(request):
    form = VariationForm()
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variationz')

    else:
        form = VariationForm()

    context = {
        'form': form
        }
    return render(request, 'adminz/addvariations.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def editvariationz(request, id):
     variations = Variation.objects.get(id=id)
     if request.method == 'POST':
        form = VariationForm(request.POST, request.FILES, instance=variations)

        if form.is_valid():
            form.save()
            return redirect('variationz')
        else:
            messages.error(request, 'invalid input')

     form = VariationForm(instance=variations)
     context = {

    'form': form,

    }
     return render(request, 'adminz/editvariationz.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def deletevariationz(request, id):
     variations = Variation.objects.get(id=id)
     variations.delete()
     return redirect('variationz')

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Vorderproducts(request,order_id):
    orderproduct = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                orderproduct=Variation.objects.filter(Q(product__product_name__icontains=keyword))


    paginator =  Paginator(orderproduct,6)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)            

    context = {
        'orderproduct': paged_orders,
        'order':order,
    }
    return render(request, 'adminz/orderproduct.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def load_subcategories(request):
    category_id = request.GET.get('category')   
    print(category_id) 
    subcategory = Sub_Category.objects.filter(category_id=category_id).order_by('id')
    return render(request, 'adminz/subcategory_drp.html.', {'subcategory': subcategory})    

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Orderz(request):
    order = Order.objects.all().order_by('-id')


    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                order=Order.objects.filter(Q(order_number__icontains=keyword) | Q(user__first_name__icontains=keyword))

    
    paginator =  Paginator(order,6)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)  

    context = {
    'order': paged_orders
    }
    return render(request, 'adminz/orders.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def EditOrder(request, id):
     orderz = Order.objects.get(id=id)
     if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=orderz)
        if form.is_valid():
            form.save()
            return redirect('orders')

        else:
            messages.error(request, 'invalid input')
            return redirect('orders')

     form = OrderForm(instance=orderz)
     context = {

    'form': form,
    'orderz': orderz,

    }
     return render(request, 'adminz/editorder.html', context)  

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def coupon(request):
    couponz = Discount.objects.all()
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                couponz=Discount.objects.filter(Q(code__icontains=keyword))


    context = {
    'couponz': couponz
    }
    return render(request, 'adminz/discount.html', context) 

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addcoupon(request):
    form = DiscountForm()
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon')

    else:
        form = DiscountForm()

    context = {
        'form': form
        }
    return render(request, 'adminz/adddiscount.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def EditCoupon(request, id):
     couponz = Discount.objects.get(id=id)
     if request.method == 'POST':
        form = DiscountForm(request.POST, request.FILES, instance=couponz)
        if form.is_valid():
            form.save()
            return redirect('coupon')

        else:
            messages.error(request, 'invalid input')
            return redirect('coupon')

     form = DiscountForm(instance=couponz)
     context = {

    'form': form,
    'couponz': couponz,

    }    
     return render(request, 'adminz/editcoupon.html', context)  

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def deletecoupon(request, id):
     couponz = Discount.objects.get(id=id)
     couponz.delete()
     return redirect('coupon')     

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Userz(request):
    userz = Account.objects.all().order_by('-id')

    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                userz=Account.objects.filter(Q(first_name__icontains=keyword))
    paginator =  Paginator(userz,3)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

  

    context = {
    'userz': paged_orders
    }
    return render(request, 'adminz/users.html', context)


@user_passes_test(lambda u: u in a, login_url='adminlogin')
def BlockUser(request,id):
    users = Account.objects.get(id=id)
    if users.is_active:
        users.is_active = False
        users.save()

    else:
         users.is_active = True
         users.save()

    return redirect('User')

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def Bannerz(request):
    banners =Banners.objects.all()
    context= {
        'banners':banners
    }    
    return render(request, 'adminz/banners.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def EditBannerz(request,id):
    banners =Banners.objects.get(id=id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banners)
        if form.is_valid():
            form.save()
            return redirect('banners')

        else:
            messages.error(request, 'invalid input')
            return redirect('orders')

    form = BannerForm(instance=banners)
    context = {

    'form': form,

    }

    return render(request, 'adminz/editbanner.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addAdmin(request,id):
    adminz = Account.objects.get(id=id)
    if request.method == 'POST':
        form = AccountForm(request.POST,request.FILES,instance=adminz)
        if form.is_valid():
            form.save()
            return redirect('User')
        else:
            messages.error(request, 'invalid input')    

   
    form = AccountForm(instance=adminz)

    context = {
        'form': form,
        'adminz':adminz
        }

  
    return render(request, 'adminz/addAdmin.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def filter_price(request):
    filter_pricez = Filter_Price.objects.all()
    if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                filter_pricez=Filter_Price.objects.filter(Q(pricerange_from__icontains=keyword))

    paginator =  Paginator(filter_pricez,8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {

       'filter_pricez': paged_products,
    }
    return render(request, 'adminz/filter_p.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def addfilter(request) :
    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('filter_price')

    else:
        form = FilterForm()

    context = {
        'form': form
        }
    return render(request, 'adminz/addfilter.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def editfilter(request,id):
    filters = Filter_Price.objects.get(id=id)
    if request.method == 'POST':
        form = FilterForm(request.POST,request.FILES,instance=filters)
        if form.is_valid():
            form.save()
            return redirect('filter_price')
        else:
            messages.error(request, 'invalid input')    
    form = FilterForm(instance=filters)

    context = {
        'form': form,}
    return render(request, 'adminz/edit_filter.html', context)

@user_passes_test(lambda u: u in a, login_url='adminlogin')
def deletefilter(request, id):
     filters = Filter_Price.objects.get(id=id)
     filters.delete()
     return redirect('filter_price')