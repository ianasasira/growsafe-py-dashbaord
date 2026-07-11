from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class RecallNotice(TenantScopedModel):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey('batches.Batch', on_delete=models.CASCADE, related_name='recalls')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='recalls')
    reason = models.TextField()
    instructions = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    affected_regions = models.JSONField(default=list, blank=True)
    initiated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='initiated_recalls')
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Recall: {self.batch.batch_number}"
