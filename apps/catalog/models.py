from django.db import models
from apps.tenants.mixins import TenantScopedModel
import uuid

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Product categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(TenantScopedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('recalled', 'Recalled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    description = models.TextField(blank=True)
    active_ingredients = models.TextField(blank=True)
    formulation = models.CharField(max_length=100, blank=True)
    packaging_variants = models.JSONField(default=list, blank=True)
    usage_instructions = models.TextField(blank=True)
    safety_information = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def batch_count(self):
        return self.batches.count()

    @property
    def total_codes(self):
        return sum(b.quantity for b in self.batches.filter(codes_generated=True))
