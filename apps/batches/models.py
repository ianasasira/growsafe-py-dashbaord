from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class Batch(TenantScopedModel):
    STATUS_CHOICES = [
        ('manufactured', 'Manufactured'),
        ('released', 'Released'),
        ('distributed', 'Distributed'),
        ('active', 'Active'),
        ('recalled', 'Recalled'),
        ('expired', 'Expired'),
        ('destroyed', 'Destroyed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_number = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='batches')
    quantity = models.IntegerField(default=0)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='manufactured')
    codes_generated = models.BooleanField(default=False)
    codes_generated_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.batch_number

    @property
    def codes_count(self):
        return self.verification_codes.count()

    @property
    def scans_count(self):
        return self.verification_codes.aggregate(total=models.Sum('scan_count'))['total'] or 0
