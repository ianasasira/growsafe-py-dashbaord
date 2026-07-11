from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ProductReport

@login_required
def complaint_list(request):
    complaints = ProductReport.objects.select_related('product', 'assigned_to').all()
    if status := request.GET.get('status'):
        complaints = complaints.filter(status=status)
    return render(request, 'dashboard/complaints/list.html', {'complaints': complaints})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(ProductReport.objects.select_related('product', 'assigned_to'), pk=pk)
    return render(request, 'dashboard/complaints/detail.html', {'complaint': complaint})

@login_required
def update_complaint(request, pk):
    complaint = get_object_or_404(ProductReport, pk=pk)
    if request.method == 'POST':
        complaint.status = request.POST.get('status', complaint.status)
        complaint.notes = request.POST.get('notes', complaint.notes)
        if complaint.status == 'resolved':
            complaint.resolved_at = timezone.now()
        complaint.save()
        messages.success(request, 'Complaint updated.')
    return redirect('complaints:detail', pk=pk)
