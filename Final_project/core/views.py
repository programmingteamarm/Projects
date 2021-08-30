from django.shortcuts import render,redirect
from core.models import Category
from core.forms import CategoryForm


def home(request):
    category = Category.objects.all()
    return render(request, 'core/index.html', {'category_list': category})


def about(request):
    return render(request, 'core/about.html')


def brand(request):
    return render(request, 'core/brand.html')


def contact(request):
    return render(request, 'core/contact.html')


def payment(request):
    return render(request, 'core/contact.html')


def guaranty(request):
    return render(request, 'core/contact.html')


def new_category(request):
    form = CategoryForm
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('home')
    context = {'form': form}
    return render(request, 'core/new_category.html', context)
# Create your views here.
