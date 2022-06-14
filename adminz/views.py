from multiprocessing import context
import re
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from store.models import Product,Variation
from.forms import ProductForm

# Create your views here.
def adminlogin(request):
      if request.method == 'POST':
        email = request.POST ['email']
        password = request.POST ['password']
       
        user = authenticate(email=email,password=password)

        if user is not None:   
            if user.is_superadmin:        
                login(request,user)
                # messages.success(request,'You are logged in')
                return redirect ('dashboard')
        else:
            messages.error(request,'invalid credientail')   
            return redirect('adminlogin') 

    
      return render (request,'adminz/adminlogin.html')

def adminhome(request):
    return render (request,'adminz/dashboard.html')

def product(request):

    products = Product.objects.all().filter(is_available = True).order_by('-id')
    
   
    context = {
       
       'products':products,
      
    }
    

    return render (request,'adminz/products.html',context)   

def addproduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addproduct')
        else:
            messages.error(request,'invalid input')

    else:
        form = ProductForm()

    context = {
       
       'form':form,
      
    }






    return render (request,'adminz/addproduct.html',context)     