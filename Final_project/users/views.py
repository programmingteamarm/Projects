from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm, MessageForm
from core.models import Order
from django.contrib.auth.decorators import login_required


def register(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        ord_count = order.count_price()['count']
    except (Order.DoesNotExist, TypeError):
        ord_count = 0
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form,
               'order_count': ord_count}
    return render(request, "users/register.html", context)


def user_login(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        ord_count = order.count_price()['count']
    except (Order.DoesNotExist, TypeError):
        ord_count = 0
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {"form": form,
               'order_count': ord_count}
    return render(request, "users/login.html", context)


def user_logout(request):
    logout(request)
    return redirect('home')


def account(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        ord_count = order.count_price()['count']
    except (Order.DoesNotExist, TypeError):
        ord_count = 0

    orders = Order.objects.filter(user=request.user, ordered=True)

    return render(request, "users/account.html", {"orders": orders,
                                                  "user": request.user,
                                                  'order_count': ord_count})


@login_required
def contact(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        ord_count = order.count_price()['count']
    except (Order.DoesNotExist, TypeError):
        ord_count = 0
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            redirect('home ')
    return render(request, 'users/contact.html', {'form': form, 'order_count': ord_count})
