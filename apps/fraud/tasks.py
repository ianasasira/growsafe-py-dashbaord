from celery import shared_task
from .services import FraudDetectionService

@shared_task
def evaluate_fraud_rules(verification_code_id):
    from apps.verification.models import VerificationCode
    
    vcode = VerificationCode.objects.filter(id=verification_code_id).first()
    if not vcode:
        return
    
    service = FraudDetectionService()
    service.evaluate_cloning(vcode)
    service.evaluate_high_frequency(vcode)

@shared_task
def check_invalid_scan_spikes():
    from apps.verification.models import ScanEvent
    from .models import FraudAlert
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count
    
    threshold_time = timezone.now() - timedelta(hours=1)
    
    spike_ips = ScanEvent.objects.filter(
        scanned_at__gte=threshold_time,
        result='invalid'
    ).values('ip_address').annotate(
        count=Count('id')
    ).filter(count__gt=500)
    
    for item in spike_ips:
        FraudAlert.objects.create(
            alert_type='invalid_spike',
            risk_level='critical',
            company_id=None,
            details={
                'ip_address': item['ip_address'],
                'invalid_scans_1h': item['count'],
            },
        )
