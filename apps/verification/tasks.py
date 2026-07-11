from celery import shared_task
from django.utils import timezone

@shared_task(bind=True, max_retries=3, default_retry_delay=15)
def generate_batch_codes(self, batch_id):
    from apps.batches.models import Batch
    from apps.verification.models import VerificationCode
    from .services import CodeGenerationService
    
    batch = Batch.objects.get(pk=batch_id)
    code_gen = CodeGenerationService()
    
    codes = code_gen.generate_bulk(batch, batch.quantity)
    VerificationCode.objects.bulk_create(codes, batch_size=5000)
    
    batch.codes_generated = True
    batch.codes_generated_at = timezone.now()
    batch.save(update_fields=['codes_generated', 'codes_generated_at'])
    
    return f"Generated {len(codes)} codes for batch {batch.batch_number}"

@shared_task
def log_scan_event(code, verification_code_id, company_id, result, context):
    from .models import ScanEvent, VerificationCode
    
    vcode = None
    if verification_code_id:
        vcode = VerificationCode.objects.filter(id=verification_code_id).first()
    
    ScanEvent.objects.create(
        code=code,
        verification_code=vcode,
        company_id=company_id,
        result=result,
        channel=context.get('channel', 'web'),
        latitude=context.get('latitude'),
        longitude=context.get('longitude'),
        ip_address=context.get('ip_address'),
        user_agent=context.get('user_agent', ''),
    )
    
    if vcode:
        from apps.fraud.tasks import evaluate_fraud_rules
        evaluate_fraud_rules.delay(verification_code_id)

@shared_task
def check_expiring_batches():
    from apps.batches.models import Batch
    from datetime import timedelta
    
    threshold = timezone.now().date() + timedelta(days=30)
    expiring = Batch.objects.filter(
        expiry_date__lte=threshold,
        expiry_date__gte=timezone.now().date(),
        status__in=['active', 'released', 'distributed']
    )
    
    for batch in expiring:
        from apps.notifications.services import NotificationService
        NotificationService().notify_expiring_batch(batch)
