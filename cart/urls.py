
from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, checkout_view

app_name = 'cart'

urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
]