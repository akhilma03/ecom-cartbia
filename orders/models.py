from django.db import models
from pytz import country_names
from accounts.models import Account
from store.models import Product,Variation

# Create your models here.

class Payment(models.Model):
    user    =  models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id =   models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True)
    payment_method_cod  = models.CharField(max_length=100,null=True)
    amount_paid     = models.CharField(max_length=100) #this is total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.first_name
class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50,null=True)
    country =   models.CharField(max_length=50)
    state =   models.CharField(max_length=50)
    district =   models.CharField(max_length=50)
    city =   models.CharField(max_length=50,blank=True)
    pincode =   models.CharField(max_length=50,blank=True)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def address(self):
        return f"{self.address_line1} {self.address_line2}"

    def __str__(self):
        return self.first_name        

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    payment= models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=30)
    order_total = models.FloatField()
    tax     = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation,on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(  auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_price

