from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("add_product/", views.add_product, name="add_product"),
    path("login", include("account.urls")),
    path("cart", include("cart.urls")),
    path("products/", views.products_page, name="products_page"),
    path("delete/<int:product_id>/", views.delete_product, name="delete_product"),
    path("products/category/<int:category_id>/", views.product_by_category, name="product_by_category"),
    path('home_search/', views.home_search, name='home_search'),
    path('product_search/', views.product_search, name='product_search'),
]
