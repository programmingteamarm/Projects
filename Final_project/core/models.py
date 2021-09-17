from django.db import models
from django.contrib.auth.models import User


def validate_num(value):
    if value < 0:
        value = 0


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='media')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(validators=[validate_num])
    image = models.ImageField(blank=True, upload_to='media')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def get_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def count_price(self):
        c = 0
        p = 0
        for i in self.order_item.all():
            c += 1
            p += i.get_price()
        return {'count': c, 'price': p}




