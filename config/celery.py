import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('growsafe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-expiring-batches': {
        'task': 'apps.verification.tasks.check_expiring_batches',
        'schedule': 86400.0,
    },
    'check-invalid-scan-spikes': {
        'task': 'apps.fraud.tasks.check_invalid_scan_spikes',
        'schedule': 300.0,
    },
    'generate-ai-insights': {
        'task': 'apps.ai_insights.tasks.generate_ai_insights',
        'schedule': 86400.0,
    },
}
