from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from datetime import datetime

@login_required
def report_list(request):
    return render(request, 'dashboard/reports/list.html')

@login_required
def verification_report(request):
    from apps.verification.models import ScanEvent
    scans = ScanEvent.objects.all()[:100]
    return render(request, 'dashboard/reports/verification.html', {'scans': scans})

@login_required
def fraud_report(request):
    from apps.fraud.models import FraudAlert
    alerts = FraudAlert.objects.all()[:100]
    return render(request, 'dashboard/reports/fraud.html', {'alerts': alerts})

@login_required
def export_report(request, report_type):
    format_type = request.GET.get('format', 'csv')
    
    if report_type == 'verification':
        from apps.verification.models import ScanEvent
        data = ScanEvent.objects.all()[:1000]
        filename = f'verification_report_{datetime.now().strftime("%Y%m%d")}'
    elif report_type == 'fraud':
        from apps.fraud.models import FraudAlert
        data = FraudAlert.objects.all()[:1000]
        filename = f'fraud_report_{datetime.now().strftime("%Y%m%d")}'
    else:
        return HttpResponse('Invalid report type', status=400)
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)
        writer.writerow([f.name for f in data.model._meta.fields])
        for item in data:
            writer.writerow([getattr(item, f.name) for f in data.model._meta.fields])
        return response
    
    return HttpResponse('Invalid format', status=400)
