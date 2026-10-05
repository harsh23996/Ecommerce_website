# cart/urls.py
from django.urls import path, include
from .views import add_to_cart_from_home, add_to_cart_from_products, cart_page ,increase_quantity, decrease_quantity , gernrate_invoice 
from product import views
urlpatterns = [
    path('add_from_home/<int:product_id>/', add_to_cart_from_home, name='add_to_cart_from_home'),
    path('add_from_products/<int:product_id>/', add_to_cart_from_products, name='add_to_cart_from_products'),
    path('view_details/', cart_page, name='cart_page'),
    path('increase_quantity/<int:item_id>', increase_quantity, name = 'increase_quantity'),
    path('decrease_quantity/<int:item_id>', decrease_quantity, name = 'decrease_quantity'),
    path('products', views.products_page, name="products_page"),
    path('invoice/',gernrate_invoice, name='generate_invoice'),   

]