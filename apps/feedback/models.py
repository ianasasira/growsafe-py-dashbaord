from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class ConsumerFeedback(TenantScopedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verification_code = models.ForeignKey('verification.VerificationCode', on_delete=models.CASCADE, related_name='feedback')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    sentiment = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.product.name}"
