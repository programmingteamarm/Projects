from django.shortcuts import render, redirect
from core.models import Category, Order, Product, OrderItem
from core.forms import OrderForm, FilterForm, SearchForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)


def home(request):
    form = SearchForm()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            for product in Product.objects.all():
                if product.name == search:
                    return product_detail(request, product.id)
            else:
                messages.warning(request, 'Nothing found')

    try:
        order = Order.objects.get(user=request.user, ordered=False)
        ord_count = order.count_price()['count']
    except (Order.DoesNotExist, TypeError):
        ord_count = 0
    context = {
        "category": Category.objects.all(),
        "order_count": ord_count,
        'form': form
    }

    return render(request, 'core/index.html', context)


def products_view(request, cat_id):
    form = FilterForm()
    filters = False
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['greater'] < form.cleaned_data['lower']:
                filters = form.cleaned_data
            else:
                messages.warning(request, 'Invalid filters')
    try:
        category = Category.objects.get(id=cat_id)
        products = Product.objects.filter(category=category)
        if filters:
            for product in Product.objects.filter(category=category):
                if (product.price < filters['greater']) or (product.price > filters['lower']):
                    products = products.exclude(id=product.id)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            ord_count = order.count_price()['count']
        except (Order.DoesNotExist, TypeError):
            ord_count = 0

        context = {
            "products": products,
            "order_count": ord_count,
            'form': form

                   }
        return render(request, 'core/product.html', context)
    except Category.DoesNotExist:
        return redirect('home')

@login_required
def add_to_cart(request, product_id, quantity=1):
    product = Product.objects.get(id=product_id)
    if product.quantity > 0:
        user_order, created = Order.objects.get_or_create(user=request.user, ordered=False)
        order_item, item_created = OrderItem.objects.get_or_create(product=product, user=request.user, ordered=False)
        if order_item in user_order.order_item.all():
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item.quantity = quantity
            user_order.order_item.add(order_item)
            user_order.save()
    else:
        messages.warning(request, 'Product limit ended')
    return redirect('products-view', product.category.id)


def product_detail(request, product_id):
    form = OrderForm

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            product = Product.objects.get(id=product_id)
            try:
                order_item = OrderItem.objects.get(user_id=request.user.id, product=product, ordered=False)
                quantity_1 = order_item.quantity
            except OrderItem.DoesNotExist:
                quantity_1 = 0
            if (model.quantity + quantity_1) <= product.quantity:
                add_to_cart(request, product_id, quantity=model.quantity)
                messages.success(request, 'Added successfully')
            else:
                messages.warning(request, 'Product limit ended')

    try:
        product = Product.objects.get(id=product_id)
        related = Product.objects.filter(category=product.category).exclude(id=product_id)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            ord_count = order.count_price()['count']
        except (Order.DoesNotExist, TypeError):
            ord_count = 0
        context = {
            "product": product,
            "related": related,
            "order_count": ord_count,
            "form": form,

        }
        return render(request, 'core/product-detail.html', context)
    except Product.DoesNotExist:
        redirect('home')


@login_required
def cart(request):


    try:
        order = Order.objects.get(user=request.user, ordered=False)

        context = {
            'order': order.order_item.all(),
            "order_count": order.count_price()['count'],
            'order_price': order.count_price()['price'],

    }
    except Order.DoesNotExist:
        context = {
            'order': [],
            "order_count": 0,

    }
    except Order.DoesNotExist:
        pass
    return render(request, 'core/cart.html', context)


def delete_order_item(request, order_item_id):
    try:
        order_item = OrderItem.objects.get(id=order_item_id)
    except OrderItem.DoesNotExist:
        return redirect("home")
    order_item.delete()
    return redirect("cart")


def buy(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order.ordered = True
    order.created_at = datetime.now()
    order.save()
    order_items = ''
    for order_item in order.order_item.all():
        order_item.product.quantity -= order_item.quantity
        order_item.product.save()
        order_item.ordered = True
        order_item.save()
        order_items += f"{order_item.product.name} - x{order_item.quantity}\n"

    email('From Shop', f'Your order confirmed successfully\n {order_items}', [request.user.email])
    return redirect('cart')



