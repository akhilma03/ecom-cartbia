from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.homei,name='home'),
    path('shop/', views.shop,name='shop'),
    path('category/<slug:category_slug>/', views.shop,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>', views.shop,name='products_by_subcategory'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.product_details,name='product_details'),
    path('search/', views.search,name='search'),
    path('fillter_price/', views.filter_price,name='filter_price'),
    path('cart/', views.cart,name='cart'),
    path('addcart/<int:product_id>/', views.addcart,name='addcart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart,name='remove_cart'),
    path('remove_items/<int:product_id>/<int:cart_item_id>/', views.remove_items,name='remove_items'),
    path('checkout/', views.checkout,name='checkout'),

     
] + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)