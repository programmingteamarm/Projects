from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('brand/', views.brand, name='brand'),
    path('contact/', views.contact, name='contact'),
    path('guaranty/', views.guaranty, name='guaranty'),
    path('payment/', views.payment, name='payment'),
    path('new_category/', views.new_category, name='new_category')
]
