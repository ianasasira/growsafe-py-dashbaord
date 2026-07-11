import math
from django.utils import timezone
from datetime import timedelta

class FraudDetectionService:
    def evaluate_cloning(self, vcode):
        from apps.verification.models import ScanEvent
        from .models import FraudAlert
        
        recent = ScanEvent.objects.filter(
            code=vcode.code,
            scanned_at__gte=timezone.now() - timedelta(minutes=30)
        )
        recent = list(recent)
        
        for i, a in enumerate(recent):
            for b in recent[i + 1:]:
                distance_km = self._haversine(
                    a.latitude, a.longitude, b.latitude, b.longitude
                )
                if distance_km > 50:
                    FraudAlert.objects.create(
                        alert_type='code_cloning',
                        risk_level='high',
                        verification_code=vcode,
                        batch=vcode.batch,
                        product=vcode.batch.product,
                        company=vcode.company,
                        details={
                            'scan_ids': [a.id, b.id],
                            'distance_km': round(distance_km, 1),
                        },
                        locations=[
                            {'lat': float(a.latitude), 'lng': float(a.longitude)},
                            {'lat': float(b.latitude), 'lng': float(b.longitude)},
                        ],
                        scan_ids=[a.id, b.id],
                    )
                    return
    
    def evaluate_high_frequency(self, vcode):
        from apps.verification.models import ScanEvent
        from .models import FraudAlert
        
        count = ScanEvent.objects.filter(
            code=vcode.code,
            scanned_at__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        if count > 20:
            FraudAlert.objects.create(
                alert_type='high_frequency',
                risk_level='medium',
                verification_code=vcode,
                batch=vcode.batch,
                product=vcode.batch.product,
                company=vcode.company,
                details={'scan_count_24h': count},
            )
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        if not lat1 or not lat2:
            return 0
        r = 6371
        d_lat = math.radians(float(lat2) - float(lat1))
        d_lon = math.radians(float(lon2) - float(lon1))
        a = (math.sin(d_lat / 2) ** 2 + 
             math.cos(math.radians(float(lat1))) * 
             math.cos(math.radians(float(lat2))) * 
             math.sin(d_lon / 2) ** 2)
        return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
