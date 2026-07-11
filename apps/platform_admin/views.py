from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.tenants.models import Company
from apps.catalog.models import Product
from apps.verification.models import ScanEvent

@role_required('superadmin')
def platform_overview(request):
    companies = Company.objects.all()
    total_products = Product.objects.count()
    total_scans = ScanEvent.objects.count()
    
    return render(request, 'platform_admin/overview.html', {
        'companies': companies,
        'total_companies': companies.count(),
        'total_products': total_products,
        'total_scans': total_scans,
    })

@role_required('superadmin')
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'platform_admin/companies/list.html', {'companies': companies})

@role_required('superadmin')
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    products = Product.objects.filter(company=company)
    users = company.users.all()
    
    return render(request, 'platform_admin/companies/detail.html', {
        'company': company,
        'products': products,
        'users': users,
    })

@role_required('superadmin')
def suspend_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.status = 'suspended'
        company.save()
    return redirect('platform_admin:company_detail', pk=pk)

@role_required('superadmin')
def platform_analytics(request):
    return render(request, 'platform_admin/analytics.html')
