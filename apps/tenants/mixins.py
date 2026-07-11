import contextvars

from django.db import models

_current_request = contextvars.ContextVar('current_request', default=None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _current_request.set(request)
        response = self.get_response(request)
        return response

def get_current_request():
    return _current_request.get()

def get_current_user():
    request = get_current_request()
    if request and hasattr(request, 'user'):
        return request.user
    return None

class TenantManager(models.Manager):
    def get_queryset(self):
        from apps.accounts.models import User
        qs = super().get_queryset()
        user = get_current_user()
        if user and user.is_authenticated and user.role != 'superadmin' and user.company_id:
            qs = qs.filter(company_id=user.company_id)
        return qs

class TenantScopedModel(models.Model):
    company = models.ForeignKey('tenants.Company', on_delete=models.CASCADE, related_name='%(class)s_set')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.company_id and user and user.is_authenticated and user.company_id:
            self.company_id = user.company_id
        super().save(*args, **kwargs)
