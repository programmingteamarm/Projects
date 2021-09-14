from django.shortcuts import render, redirect
from core.models import Category, Order, Product, OrderItem


def home(request):

    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except Order.DoesNotExist:
        order = 0
    context = {
        "category": Category.objects.all(),
        "order_count": order.count_price()['count'],
        "order": order.order_item.all()
    }
    return render(request, 'core/index.html', context)


def products_view(request, cat_id):

    try:
        category = Category.objects.get(id=cat_id)
        products = Product.objects.filter(category=category)
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            "order": order.order_item.all(),
            "products": products,
            "category": Category.objects.all(),
            "order_count": order.count_price()['count'],

                   }
        return render(request, 'core/product.html', context)
    except Category.DoesNotExist:
        return redirect('home')


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        related = Product.objects.filter(category=product.category).exclude(id=product_id)
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            "product": product,
            "related": related,
            "category": Category.objects.all(),
            "order_count": order.count_price()['count'],

        }
        return render(request, 'core/product-detail.html', context)
    except Product.DoesNotExist:
        redirect('home')


def add_to_cart(request, product_id):
    user_order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    product = Product.objects.get(id=product_id)
    order_item, item_created = OrderItem.objects.get_or_create(product=product, user=request.user, ordered=False)
    if order_item in user_order.order_item.all():
        order_item.quantity += 1
        order_item.save()
    else:
        user_order.order_item.add(order_item)
        user_order.save()
    return redirect('home')


def cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'category': Category.objects.all(),
        'order': order.order_item.all(),
        "order_count": order.count_price()['count'],
        'order_price': order.count_price()['price']
    }
    return render(request, 'core/cart.html', context)
