from django.contrib import admin
from core.models import Category, Order, Product, OrderItem

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
# Register your models here.
