from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products_view/<int:cat_id>', views.products_view, name='products-view'),
    path('product_detail/<int:product_id>', views.product_detail, name='product-detail'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add'),
    path('remove_from_cart/<int:order_item_id>', views.delete_order_item, name='remove'),
    path('cart/', views.cart, name='cart'),
    path('buy/',  views.buy, name='buy'),


]
