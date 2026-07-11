from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Batch
from .forms import BatchForm
from .services import BatchNumberGenerator
from apps.verification.tasks import generate_batch_codes

@login_required
def batch_list(request):
    batches = Batch.objects.select_related('product').all()
    
    if q := request.GET.get('q'):
        batches = batches.filter(batch_number__icontains=q)
    if status := request.GET.get('status'):
        batches = batches.filter(status=status)
    
    return render(request, 'dashboard/batches/list.html', {'batches': batches})

@login_required
def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.batch_number = BatchNumberGenerator().generate(batch)
            batch.save()
            messages.success(request, f'Batch {batch.batch_number} created successfully.')
            return redirect('batches:detail', pk=batch.pk)
    else:
        form = BatchForm()
    
    return render(request, 'dashboard/batches/form.html', {'form': form})

@login_required
def batch_detail(request, pk):
    batch = get_object_or_404(Batch.objects.select_related('product'), pk=pk)
    return render(request, 'dashboard/batches/detail.html', {'batch': batch})

@login_required
def generate_codes(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    
    if request.method == 'POST':
        if batch.codes_generated:
            messages.warning(request, 'Codes already generated for this batch.')
        else:
            generate_batch_codes.delay(str(batch.id))
            messages.success(request, 'Code generation started. This may take a few minutes.')
        return redirect('batches:detail', pk=pk)
    
    return render(request, 'dashboard/batches/generate.html', {'batch': batch})

@login_required
def export_codes(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    format_type = request.GET.get('format', 'csv')
    
    if format_type == 'csv':
        from apps.reports.services import ReportExportService
        return ReportExportService().export_batch_codes_csv(batch)
    elif format_type == 'pdf':
        from apps.reports.services import ReportExportService
        return ReportExportService().export_batch_codes_pdf(batch)
    
    return redirect('batches:detail', pk=pk)
