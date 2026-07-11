from django.db import models
from apps.tenants.mixins import TenantScopedModel
from django.utils import timezone

class VerificationCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    batch = models.ForeignKey('batches.Batch', on_delete=models.CASCADE, related_name='verification_codes')
    company = models.ForeignKey('tenants.Company', on_delete=models.CASCADE, related_name='verification_codes')
    scan_count = models.IntegerField(default=0)
    first_scanned_at = models.DateTimeField(null=True, blank=True)
    last_scanned_at = models.DateTimeField(null=True, blank=True)
    qr_image_path = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    all_objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['batch', 'is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.code

class ScanEvent(models.Model):
    RESULT_CHOICES = [
        ('genuine', 'Genuine'),
        ('already_used', 'Already Used'),
        ('recalled', 'Recalled'),
        ('invalid', 'Invalid'),
        ('expired', 'Expired'),
    ]
    CHANNEL_CHOICES = [
        ('qr', 'QR Code'),
        ('sms', 'SMS'),
        ('ussd', 'USSD'),
        ('web', 'Web'),
    ]

    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, db_index=True)
    verification_code = models.ForeignKey(VerificationCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='scan_events')
    company = models.ForeignKey('tenants.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='scan_events')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='qr')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    scanned_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = models.Manager()
    all_objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['code', 'scanned_at']),
            models.Index(fields=['company', 'scanned_at']),
            models.Index(fields=['result', 'scanned_at']),
        ]
        ordering = ['-scanned_at']

    def __str__(self):
        return f"{self.code} - {self.result}"
