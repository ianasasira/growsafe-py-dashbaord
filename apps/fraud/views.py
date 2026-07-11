from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FraudAlert

@login_required
def fraud_list(request):
    alerts = FraudAlert.objects.select_related('product', 'batch').all()
    
    if risk := request.GET.get('risk'):
        alerts = alerts.filter(risk_level=risk)
    if status := request.GET.get('status'):
        alerts = alerts.filter(status=status)
    if alert_type := request.GET.get('type'):
        alerts = alerts.filter(alert_type=alert_type)
    
    return render(request, 'dashboard/fraud/list.html', {'alerts': alerts})

@login_required
def fraud_detail(request, pk):
    alert = get_object_or_404(FraudAlert.objects.select_related('product', 'batch'), pk=pk)
    return render(request, 'dashboard/fraud/detail.html', {'alert': alert})

@login_required
def resolve_alert(request, pk):
    alert = get_object_or_404(FraudAlert, pk=pk)
    if request.method == 'POST':
        alert.status = 'resolved'
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.notes = request.POST.get('notes', '')
        alert.save()
        messages.success(request, 'Alert resolved.')
    return redirect('fraud:detail', pk=pk)

@login_required
def dismiss_alert(request, pk):
    alert = get_object_or_404(FraudAlert, pk=pk)
    if request.method == 'POST':
        alert.status = 'dismissed'
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.save()
        messages.success(request, 'Alert dismissed.')
    return redirect('fraud:list')
