from django import forms
from core.models import OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity', )


class FilterForm(forms.Form):
    greater = forms.FloatField()
    lower = forms.FloatField()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)
