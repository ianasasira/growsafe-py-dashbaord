from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import RecallNotice
from .forms import RecallForm

@login_required
def recall_list(request):
    recalls = RecallNotice.objects.select_related('batch__product', 'initiated_by').all()
    return render(request, 'dashboard/recalls/list.html', {'recalls': recalls})

@login_required
def recall_create(request):
    if request.method == 'POST':
        form = RecallForm(request.POST)
        if form.is_valid():
            recall = form.save(commit=False)
            recall.initiated_by = request.user
            recall.save()
            recall.batch.status = 'recalled'
            recall.batch.save()
            messages.success(request, 'Recall initiated.')
            return redirect('recalls:detail', pk=recall.pk)
    else:
        form = RecallForm()
    return render(request, 'dashboard/recalls/form.html', {'form': form})

@login_required
def recall_detail(request, pk):
    recall = get_object_or_404(RecallNotice.objects.select_related('batch__product'), pk=pk)
    return render(request, 'dashboard/recalls/detail.html', {'recall': recall})
