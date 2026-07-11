from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SupplyChainPartner, ProductJourney
from .forms import PartnerForm

@login_required
def partner_list(request):
    partners = SupplyChainPartner.objects.all()
    return render(request, 'dashboard/supply_chain/list.html', {'partners': partners})

@login_required
def partner_create(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supply_chain:list')
    else:
        form = PartnerForm()
    return render(request, 'dashboard/supply_chain/form.html', {'form': form})

@login_required
def partner_detail(request, pk):
    partner = get_object_or_404(SupplyChainPartner, pk=pk)
    return render(request, 'dashboard/supply_chain/detail.html', {'partner': partner})

@login_required
def product_journey(request, code_id):
    from apps.verification.models import VerificationCode
    vcode = get_object_or_404(VerificationCode, pk=code_id)
    journey = ProductJourney.objects.filter(verification_code=vcode).order_by('timestamp')
    return render(request, 'dashboard/supply_chain/journey.html', {
        'vcode': vcode,
        'journey': journey,
    })
