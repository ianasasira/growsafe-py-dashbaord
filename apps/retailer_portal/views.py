from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def retailer_dashboard(request):
    return render(request, 'dashboard/retailers/dashboard.html')

@login_required
def stock_verification(request):
    return render(request, 'dashboard/retailers/stock.html')

@login_required
def report_issue(request):
    return render(request, 'dashboard/retailers/report.html')
