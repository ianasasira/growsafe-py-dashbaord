import re
from django.utils import timezone
from datetime import timedelta

class AiInsightService:
    def generate_fraud_insight(self, company):
        from apps.fraud.models import FraudAlert
        
        this_week = FraudAlert.objects.filter(
            company=company,
            created_at__gte=timezone.now() - timedelta(weeks=1)
        ).count()
        
        last_week = FraudAlert.objects.filter(
            company=company,
            created_at__range=(
                timezone.now() - timedelta(weeks=2),
                timezone.now() - timedelta(weeks=1)
            )
        ).count()
        
        if last_week == 0:
            return None
        
        change = round(((this_week - last_week) / last_week) * 100)
        if abs(change) < 10:
            return None
        
        direction = "increased" if change > 0 else "decreased"
        return f"Counterfeit activity {direction} {abs(change)}% this week, with {this_week} new fraud alerts detected."

class AiQueryService:
    def process_query(self, query, company):
        query_lower = query.lower()
        
        if 'fraud' in query_lower or 'counterfeit' in query_lower:
            from apps.fraud.models import FraudAlert
            count = FraudAlert.objects.filter(company=company).count()
            return {'answer': f"There are {count} fraud alerts in the system.", 'type': 'fraud'}
        
        elif 'scan' in query_lower or 'verification' in query_lower:
            from apps.verification.models import ScanEvent
            count = ScanEvent.objects.filter(company=company).count()
            return {'answer': f"There have been {count} verification scans.", 'type': 'verification'}
        
        elif 'product' in query_lower:
            from apps.catalog.models import Product
            count = Product.objects.filter(company=company).count()
            return {'answer': f"There are {count} products in the catalog.", 'type': 'product'}
        
        elif 'batch' in query_lower:
            from apps.batches.models import Batch
            count = Batch.objects.filter(company=company).count()
            return {'answer': f"There are {count} batches in the system.", 'type': 'batch'}
        
        else:
            return {'answer': "I can help with queries about fraud, scans, products, or batches. Try asking 'How many fraud alerts are there?'", 'type': 'general'}
