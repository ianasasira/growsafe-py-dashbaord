from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings/index.html')

@login_required
def company_settings(request):
    if request.method == 'POST':
        company = request.company
        company.name = request.POST.get('name', company.name)
        company.save()
    return render(request, 'dashboard/settings/company.html')

@login_required
def user_management(request):
    from apps.accounts.models import User
    users = User.objects.filter(company=request.company)
    return render(request, 'dashboard/settings/users.html', {'users': users})

@login_required
def verification_settings(request):
    return render(request, 'dashboard/settings/verification.html')
