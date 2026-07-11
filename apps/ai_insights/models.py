from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class AiInsight(TenantScopedModel):
    CATEGORY_CHOICES = [
        ('fraud', 'Fraud'),
        ('verification', 'Verification'),
        ('supply_chain', 'Supply Chain'),
        ('product', 'Product'),
        ('general', 'General'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    insight_text = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
