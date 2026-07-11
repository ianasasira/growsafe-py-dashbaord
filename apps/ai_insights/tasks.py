from celery import shared_task

@shared_task
def generate_ai_insights():
    from apps.tenants.models import Company
    from apps.ai_insights.models import AiInsight
    from .services import AiInsightService
    
    service = AiInsightService()
    
    for company in Company.objects.filter(status='active'):
        insight_text = service.generate_fraud_insight(company)
        if insight_text:
            AiInsight.objects.create(
                category='fraud',
                title='Weekly Fraud Trend',
                insight_text=insight_text,
                company=company,
            )
