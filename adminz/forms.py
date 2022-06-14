from django import forms
from accounts.models import Account
from store.models import Product,Category,Sub_Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields =['product_name','description','price','images','images1','images2','images3','stock','is_available','category','sub_category',]
   