from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'image',]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-black'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-black'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-black'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-black'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-2 border border-black'
            }),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address','zipcode', 'payment_method']