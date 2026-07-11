from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class SupplyChainPartner(TenantScopedModel):
    TYPE_CHOICES = [
        ('distributor', 'Distributor'),
        ('wholesaler', 'Wholesaler'),
        ('retailer', 'Retailer'),
        ('warehouse', 'Warehouse'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    partner_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    region = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class ProductJourney(TenantScopedModel):
    STAGE_CHOICES = [
        ('factory', 'Factory'),
        ('warehouse', 'Warehouse'),
        ('distributor', 'Distributor'),
        ('wholesaler', 'Wholesaler'),
        ('retailer', 'Retailer'),
        ('consumer', 'Consumer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verification_code = models.ForeignKey('verification.VerificationCode', on_delete=models.CASCADE, related_name='journey_events')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    partner = models.ForeignKey(SupplyChainPartner, on_delete=models.SET_NULL, null=True, blank=True, related_name='journey_events')
    location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.verification_code.code} - {self.stage}"
