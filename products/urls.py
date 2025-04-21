from django.urls import path

from products.views import product_list, create_product, my_products, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('my-products/', my_products, name='my_products'),
path('product/<int:pk>/', product_detail, name='product_detail'),
]