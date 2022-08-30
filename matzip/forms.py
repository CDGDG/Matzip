from django import forms
from matzip.models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", 'type', 'address', 'phone']
