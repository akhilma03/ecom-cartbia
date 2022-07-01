from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.adminlogin,name='adminlogin'),
    path('home/', views.adminhome,name='dashboard'),
     path('adminlogout/', views.adminlogout,name='adminlogout'),
 
  
   
    path('productz/', views.product,name='product'),
    path('addproduct/', views.addproduct,name='addproduct'),
    path('addcategory/', views.addcategory,name='addcategory'),
    path('edit_category/<str:slug>/', views.edit_category,name='edit_category'),
    path('category/', views.category,name='category'),
    path('Deletecategory/<str:slug>/', views.Deletecategory,name='Deletecategory'),


    path('addsubcategory/', views.addsubcategory,name='addsubcategory'),

    # path('edit_subcategory/<str:slug>/<str:slug>/', views.edit_subcategory,name='edit_subcategory'), 
    path('Deletesubcategory/<str:slug>/', views.Deletesubcategory,name='Deletesubcategory'),
    path('subcategory/', views.subcategory,name='subcategory'),
    path('edits/<str:slug>/', views.editS,name='editsubcategory'),

     path('<int:id>/editproduct/', views.edit_products,name='editproduct'),
     path('productdetails/', views.productsdetails,name='productdetails'),
     path('<int:id>/deleteproduct/', views.deleteproduct,name='deleteproduct'),

     path('variationz/', views.variationz,name='variationz'),
     path('addvariationz/', views.addvariationz,name='addvariationz'),
     path('<int:id>/editvariationz/', views.editvariationz,name='editvariationz'),
     path('<int:id>/deletevariationz/', views.deletevariationz,name='deletevariationz'),
     path('<int:order_id>/orderproducts/', views.Vorderproducts,name='orderproducts'),
     path('orders/', views.Orderz,name='orders'),
     path('<int:id>/EditOrder/', views.EditOrder,name='EditOrder'),
     path('User/', views.Userz,name='User'),
     path('<int:id>/addAdmin/',views.addAdmin,name='addAdmin'),
     path('<int:id>/BlockUser/', views.BlockUser,name='BlockUser'),
    #  path('<int:id>/UnBlockUser/', views.UnBlockUser,name='UnBlockUser'),
     path('ajax/load_subcategories/', views.load_subcategories, name='ajax_load_subcategories'),

    path('banners/', views.Bannerz,name='banners'),
    path('<int:id>/banners/', views.EditBannerz,name='Editbanners'),
     path('coupon/', views.coupon,name='coupon'),
     path('addcoupon/', views.addcoupon,name='addcoupon'),
      path('<int:id>/EditCoupon/', views.EditCoupon,name='EditCoupon'), 
      path('<int:id>/deletecoupon/',views.deletecoupon,name='deletecoupon'),
  
       path('filter_price/', views.filter_price, name='filter_price'),
  
       path('<int:id>/editfilter/', views.editfilter, name='editfilter'),
  
       path('<int:id>/deletefilter/', views.deletefilter, name='deletefilter'),
          path('addfilter/', views.addfilter,name='addfilter'),

 
     
] + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)