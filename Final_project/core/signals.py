from .models import Users_orders, Order
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def create_orders(instance, created, sender, **kwargs):
    if created:
        Users_orders.objects.create(user_id=instance.id)


post_save.connect(receiver=create_orders, sender=User)


def add_order(instance, created, sender, **kwargs):
    if created:
        user_orders = Users_orders.objects.get(user_id=instance.user_id)
        user_orders.orders_ids.add(instance.id)


post_save.connect(receiver=add_order, sender=Order)