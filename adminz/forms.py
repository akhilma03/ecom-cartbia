
from django import forms
from . models import Banners
from store.models import Product,Category,Sub_Category,Variation,Filter_Price
from orders.models import Order,Discount
from accounts.models import Account

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields =['product_name','slug','description','price','images','images1','images2','images3','stock','is_available','category','sub_category',]
    
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class':'form-control'})
        self.fields['slug'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['price'].widget.attrs.update({'class':'form-control'})
        self.fields['images'].widget.attrs.update({'class':'form-control'})
        self.fields['images1'].widget.attrs.update({'class':'form-control'})
        self.fields['images2'].widget.attrs.update({'class':'form-control'})
        self.fields['images3'].widget.attrs.update({'class':'form-control'})
        self.fields['stock'].widget.attrs.update({'class':'form-control'})
        
        self.fields['category'].widget.attrs.update({'class':'form-control'})
        self.fields['sub_category'].widget.attrs.update({'class':'form-control'})

        # super().__init__(*args, **kwargs)
        # self.fields['sub_category'].queryset = Sub_Category.objects.none()

        # if 'category' in self.data:
        #     try:
        #         category_id = int(self.data.get('category'))
        #         self.fields['sub_category'].queryset = Sub_Category.objects.filter(category_id=category_id).order_by('id')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['sub_category'].queryset = self.instance.category.sub_category_set.order_by('id')
       


        


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs.update({'class':'form-control'})    
        self.fields['slug'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})


class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category

        fields ='__all__'
    def __init__(self, *args, **kwargs):
        super(Sub_CategoryForm,self).__init__(*args, **kwargs)
        self.fields['sub_categoryname'].widget.attrs.update({'class':'form-control'})    
        self.fields['slug'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})    
        self.fields['category'].widget.attrs.update({'class':'form-control'})    

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation    

        fields = '__all__'  
    def __init__(self, *args, **kwargs):
        super(VariationForm,self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class':'form-control'})    
        self.fields['variation_category'].widget.attrs.update({'class':'form-control'})
        self.fields['variation_value'].widget.attrs.update({'class':'form-control'})    
          
      

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = ['status',] 
    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields['status'].widget.attrs.update({'class':'form-control'})

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banners

        fields = '__all__'  
 
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['code','discount_percentage','discount_from','is_active', ] 

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['is_admin','is_active','is_superadmin','is_staff',]         

class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter_Price
        fields = '__all__'
     
