from django import forms
from .models import SupplyChainPartner

class PartnerForm(forms.ModelForm):
    class Meta:
        model = SupplyChainPartner
        fields = ['name', 'partner_type', 'region', 'district', 'contact_person', 
                  'phone', 'email', 'latitude', 'longitude', 'status']
