from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.analytics.urls')),
    path('dashboard/products/', include('apps.catalog.urls')),
    path('dashboard/batches/', include('apps.batches.urls')),
    path('dashboard/fraud/', include('apps.fraud.urls')),
    path('dashboard/supply-chain/', include('apps.supply_chain.urls')),
    path('dashboard/complaints/', include('apps.complaints.urls')),
    path('dashboard/recalls/', include('apps.recalls.urls')),
    path('dashboard/reports/', include('apps.reports.urls')),
    path('dashboard/ai-insights/', include('apps.ai_insights.urls')),
    path('dashboard/settings/', include('apps.accounts.settings_urls')),
    path('dashboard/notifications/', include('apps.notifications.urls')),
    path('dashboard/retailers/', include('apps.retailer_portal.urls')),
    path('platform/', include('apps.platform_admin.urls')),
    path('v/<str:code>/', include('apps.verification.urls')),
    path('api/v1/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
