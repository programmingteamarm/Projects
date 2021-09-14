from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products_view/<int:cat_id>', views.products_view, name='products-view'),
    path('product_detail/<int:product_id>', views.product_detail, name='product-detail'),
    path('add_to_cart/<product_id>', views.add_to_cart, name='add'),
    path('cart/>', views.cart, name='cart')
]
