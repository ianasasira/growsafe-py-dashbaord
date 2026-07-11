from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'category', 'description', 'active_ingredients', 
                  'formulation', 'packaging_variants', 'usage_instructions', 
                  'safety_information', 'image', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'active_ingredients': forms.Textarea(attrs={'rows': 2}),
            'usage_instructions': forms.Textarea(attrs={'rows': 3}),
            'safety_information': forms.Textarea(attrs={'rows': 3}),
        }
