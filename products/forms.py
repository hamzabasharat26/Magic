from django import forms
from .models import PurchaseOrder, Product

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'date', 'brand', 'origin_country', 'article_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all'}),
            'po_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all', 'placeholder': 'Enter PO Number'}),
            'brand': forms.Select(attrs={'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all'}),
            'origin_country': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all', 'placeholder': 'Enter Origin/Country'}),
            'article_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all'}),
        }
        labels = {
            'po_number': 'PO Number',
            'origin_country': 'Origin/Country',
            'article_type': 'Article Type',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['size', 'quantity', 'color']
        widgets = {
            'size': forms.Select(attrs={'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all', 'id': 'size-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all', 
                'placeholder': 'Enter quantity',
                'min': '1'
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all', 
                'placeholder': 'Enter color'
            }),
        }