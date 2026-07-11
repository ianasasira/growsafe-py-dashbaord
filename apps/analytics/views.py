from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

@login_required
def overview(request):
    company = request.company
    user = request.user
    
    cache_key = f'dashboard_overview_{company.id if company else "all"}'
    data = cache.get(cache_key)
    
    if not data:
        from apps.catalog.models import Product
        from apps.batches.models import Batch
        from apps.verification.models import VerificationCode, ScanEvent
        from apps.fraud.models import FraudAlert
        from apps.recalls.models import RecallNotice
        
        if user.role == 'superadmin':
            products_qs = Product.objects.all()
            batches_qs = Batch.objects.all()
            codes_qs = VerificationCode.objects.all()
            scans_qs = ScanEvent.objects.all()
            fraud_qs = FraudAlert.objects.all()
            recalls_qs = RecallNotice.objects.filter(status='active')
        else:
            products_qs = Product.objects.filter(company=company)
            batches_qs = Batch.objects.filter(company=company)
            codes_qs = VerificationCode.objects.filter(company=company)
            scans_qs = ScanEvent.objects.filter(company=company)
            fraud_qs = FraudAlert.objects.filter(company=company)
            recalls_qs = RecallNotice.objects.filter(company=company, status='active')
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        data = {
            'total_products': products_qs.count(),
            'active_batches': batches_qs.filter(status__in=['active', 'released', 'distributed']).count(),
            'total_codes': codes_qs.count(),
            'total_scans': scans_qs.count(),
            'fraud_alerts': fraud_qs.count(),
            'critical_alerts': fraud_qs.filter(risk_level='critical').count(),
            'verified_today': scans_qs.filter(scanned_at__date=today).count(),
            'active_recalls': recalls_qs.count(),
            'recent_scans': scans_qs.select_related('verification_code__batch__product').order_by('-scanned_at')[:10],
            'scan_trend': list(scans_qs.filter(scanned_at__gte=today-timedelta(days=30)).values('scanned_at__date').annotate(count=Count('id')).order_by('scanned_at__date')),
            'channel_split': {
                'qr': scans_qs.filter(channel='qr').count(),
                'sms': scans_qs.filter(channel='sms').count(),
                'ussd': scans_qs.filter(channel='ussd').count(),
            },
        }
        cache.set(cache_key, data, 60)
    
    return render(request, 'dashboard/overview.html', data)
