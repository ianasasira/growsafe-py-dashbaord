from django import forms
from .models import RecallNotice

class RecallForm(forms.ModelForm):
    class Meta:
        model = RecallNotice
        fields = ['batch', 'product', 'reason', 'instructions', 'severity', 'affected_regions']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }
