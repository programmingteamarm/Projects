from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.ImageField(default='static/core/default_image.png', blank=True, null=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)


class Users_orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    orders_ids = models.ManyToManyField(Order)

