from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class FraudAlert(TenantScopedModel):
    TYPE_CHOICES = [
        ('code_cloning', 'Code Cloning'),
        ('high_frequency', 'High Frequency'),
        ('invalid_spike', 'Invalid Scan Spike'),
        ('geo_anomaly', 'Geographic Anomaly'),
    ]
    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    verification_code = models.ForeignKey('verification.VerificationCode', on_delete=models.CASCADE, null=True, blank=True, related_name='fraud_alerts')
    batch = models.ForeignKey('batches.Batch', on_delete=models.CASCADE, null=True, blank=True, related_name='fraud_alerts')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, null=True, blank=True, related_name='fraud_alerts')
    details = models.JSONField(default=dict, blank=True)
    locations = models.JSONField(default=list, blank=True)
    scan_ids = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'risk_level']),
        ]

    def __str__(self):
        return f"{self.alert_type} - {self.risk_level}"

    @property
    def risk_score(self):
        scores = {'low': 25, 'medium': 50, 'high': 75, 'critical': 100}
        return scores.get(self.risk_level, 0)
