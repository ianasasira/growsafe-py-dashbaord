from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
import random
import uuid

class Command(BaseCommand):
    help = 'Seed Bukoola Chemicals data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Bukoola Chemicals data...')
        
        from apps.tenants.models import Company
        from apps.accounts.models import User
        from apps.catalog.models import Product, ProductCategory
        from apps.batches.models import Batch
        from apps.verification.models import VerificationCode, ScanEvent
        from apps.fraud.models import FraudAlert
        from apps.supply_chain.models import SupplyChainPartner
        from apps.feedback.models import ConsumerFeedback
        from apps.complaints.models import ProductReport
        from apps.ai_insights.models import AiInsight
        
        company, _ = Company.objects.get_or_create(
            slug='bukoola',
            defaults={
                'name': 'Bukoola Chemicals',
                'country': 'Uganda',
                'plan': 'enterprise',
                'status': 'active',
                'max_products': 999999,
                'max_codes_per_month': 999999999,
            }
        )
        self.stdout.write(f'Company: {company.name}')
        
        superadmin, _ = User.objects.get_or_create(
            email='admin@growsafe.com',
            defaults={
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': 'superadmin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        superadmin.set_password('SuperAdmin@2026')
        superadmin.save()
        
        company_admin, _ = User.objects.get_or_create(
            email='admin@bukoola.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'Bukoola',
                'role': 'company_admin',
                'company': company,
            }
        )
        company_admin.set_password('Admin@2026')
        company_admin.save()
        
        staff, _ = User.objects.get_or_create(
            email='staff@bukoola.com',
            defaults={
                'first_name': 'Staff',
                'last_name': 'Member',
                'role': 'company_staff',
                'company': company,
            }
        )
        staff.set_password('Staff@2026')
        staff.save()
        
        self.stdout.write('Users created')
        
        categories_data = [
            ('Crop Protection', 'crop-protection'),
            ('Fertilizers', 'fertilizers'),
            ('Herbicides', 'herbicides'),
            ('Fungicides', 'fungicides'),
            ('Insecticides', 'insecticides'),
        ]
        categories = []
        for name, slug in categories_data:
            cat, _ = ProductCategory.objects.get_or_create(slug=slug, defaults={'name': name})
            categories.append(cat)
        
        products_data = [
            ('DUDU CYPER', 'Crop Protection', 'DC-001'),
            ('DUDU GOLD', 'Fertilizers', 'DC-002'),
            ('DUDU MATABA', 'Herbicides', 'DC-003'),
            ('DUDU THIO', 'Fungicides', 'DC-004'),
            ('DUDU DIM', 'Insecticides', 'DC-005'),
            ('DUDU SUPER', 'Crop Protection', 'DC-006'),
            ('DUDU PLUS', 'Fertilizers', 'DC-007'),
            ('DUDU FAST', 'Herbicides', 'DC-008'),
            ('DUDU MAX', 'Fungicides', 'DC-009'),
            ('DUDU PRO', 'Insecticides', 'DC-010'),
            ('DUDU POWER', 'Crop Protection', 'DC-011'),
            ('DUDU GROW', 'Fertilizers', 'DC-012'),
            ('DUDU KILL', 'Herbicides', 'DC-013'),
            ('DUDU SHIELD', 'Fungicides', 'DC-014'),
            ('DUDU FORCE', 'Insecticides', 'DC-015'),
            ('DUDU ELITE', 'Crop Protection', 'DC-016'),
            ('DUDU PRIME', 'Fertilizers', 'DC-017'),
            ('DUDU RAPID', 'Herbicides', 'DC-018'),
            ('DUDU GUARD', 'Fungicides', 'DC-019'),
            ('DUDU STORM', 'Insecticides', 'DC-020'),
        ]
        
        products = []
        for name, cat_name, sku in products_data:
            cat = next(c for c in categories if c.name == cat_name)
            product, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'category': cat,
                    'company': company,
                    'description': f'{name} - High quality agro-input product for optimal crop protection and yield.',
                    'active_ingredients': 'Active chemical compounds for effective pest and disease control',
                    'formulation': 'Emulsifiable concentrate',
                    'status': 'active',
                }
            )
            products.append(product)
        
        self.stdout.write(f'Created {len(products)} products')
        
        batches = []
        for i, product in enumerate(products):
            for j in range(3):
                batch_num = f"BKC-2026-{i*3+j+1:04d}"
                batch, _ = Batch.objects.get_or_create(
                    batch_number=batch_num,
                    defaults={
                        'product': product,
                        'company': company,
                        'quantity': random.randint(500, 2000),
                        'manufacture_date': date(2026, random.randint(1, 6), random.randint(1, 28)),
                        'expiry_date': date(2027, random.randint(1, 12), random.randint(1, 28)),
                        'status': random.choice(['active', 'released', 'distributed']),
                        'codes_generated': True,
                        'codes_generated_at': timezone.now(),
                    }
                )
                batches.append(batch)
        
        self.stdout.write(f'Created {len(batches)} batches')
        
        self.stdout.write('Generating verification codes...')
        codes = []
        code_set = set()  # local dedup
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        for batch in batches:
            prefix = batch.company.slug[:3].upper()
            year = batch.manufacture_date.year
            target = min(batch.quantity, 500)  # cap per batch for reasonable seed size
            while len(code_set) < len(codes) + target:
                payload = ''.join(random.choices(alphabet, k=8))
                code_str = f"{prefix}-{year}-{payload}"
                check = sum(ord(c) for c in code_str) % 10
                full_code = f"{code_str}-{check}"
                if full_code not in code_set:
                    code_set.add(full_code)
                    codes.append(VerificationCode(
                        code=full_code,
                        batch=batch,
                        company=company,
                        scan_count=0,
                    ))
        
        self.stdout.write(f'Bulk inserting {len(codes)} verification codes...')
        VerificationCode.objects.bulk_create(codes, ignore_conflicts=True, batch_size=5000)
        codes = list(VerificationCode.objects.filter(company=company))  # reload to get PKs
        self.stdout.write(f'Created {len(codes)} verification codes')
        
        regions = [
            ('Kampala', 0.3476, 32.5825, 0.40),
            ('Mbarara', -0.6076, 30.6548, 0.20),
            ('Gulu', 2.7747, 32.2989, 0.15),
            ('Jinja', 0.4454, 33.2042, 0.10),
            ('Mbale', 1.0814, 34.1758, 0.08),
            ('Fort Portal', 0.6674, 30.2769, 0.07),
        ]
        
        self.stdout.write('Generating scan events...')
        scan_events = []
        codes_to_update = {}
        scanned_codes = codes[:min(5000, len(codes))]
        for vc in scanned_codes:
            num_scans = random.choices([0, 1, 2, 3, 5], weights=[50, 30, 10, 5, 5])[0]
            for _ in range(num_scans):
                region_name, lat, lng, weight = random.choices(regions, weights=[r[3] for r in regions])[0]
                result = random.choices(
                    ['genuine', 'already_used', 'invalid', 'expired'],
                    weights=[85, 8, 5, 2]
                )[0]
                
                scan_events.append(ScanEvent(
                    code=vc.code,
                    verification_code=vc,
                    company=company,
                    result=result,
                    channel=random.choice(['qr', 'sms', 'ussd']),
                    latitude=lat + random.uniform(-0.05, 0.05),
                    longitude=lng + random.uniform(-0.05, 0.05),
                    ip_address=f'197.{random.randint(100,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                    scanned_at=timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)),
                ))
                
                if result in ['genuine', 'already_used']:
                    codes_to_update.setdefault(vc.pk, {'count': 0, 'first': None, 'last': None})
                    codes_to_update[vc.pk]['count'] += 1
                    now = timezone.now()
                    if codes_to_update[vc.pk]['first'] is None:
                        codes_to_update[vc.pk]['first'] = now
                    codes_to_update[vc.pk]['last'] = now
        
        ScanEvent.objects.bulk_create(scan_events, batch_size=5000)
        
        vc_bulk_updates = []
        for vc in codes:
            if vc.pk in codes_to_update:
                info = codes_to_update[vc.pk]
                vc.scan_count = info['count']
                vc.first_scanned_at = info['first']
                vc.last_scanned_at = info['last']
                vc_bulk_updates.append(vc)
        if vc_bulk_updates:
            VerificationCode.objects.bulk_update(vc_bulk_updates, ['scan_count', 'first_scanned_at', 'last_scanned_at'], batch_size=5000)
        
        self.stdout.write(f'Created {len(scan_events)} scan events')
        
        fraud_alerts = []
        for i in range(30):
            vc = random.choice(codes[:1000])
            alert, _ = FraudAlert.objects.get_or_create(
                id=uuid.uuid4(),
                defaults={
                    'alert_type': random.choice(['code_cloning', 'high_frequency', 'geo_anomaly']),
                    'risk_level': random.choice(['low', 'medium', 'high', 'critical']),
                    'status': random.choice(['open', 'investigating', 'resolved']),
                    'verification_code': vc,
                    'batch': vc.batch,
                    'product': vc.batch.product,
                    'company': company,
                    'details': {'scan_ids': [1, 2], 'distance_km': random.uniform(50, 200)},
                    'locations': [
                        {'lat': float(vc.batch.product.company_id % 10), 'lng': float(32.0)},
                    ],
                }
            )
            fraud_alerts.append(alert)
        
        self.stdout.write(f'Created {len(fraud_alerts)} fraud alerts')
        
        partner_types = ['distributor', 'wholesaler', 'retailer', 'warehouse']
        districts = ['Kampala', 'Mbarara', 'Gulu', 'Jinja', 'Mbale', 'Fort Portal', 'Arua', 'Masaka']
        
        partners = []
        for i in range(30):
            district = random.choice(districts)
            region_name, lat, lng, _ = next((r for r in regions if r[0] == district), regions[0])
            partner, _ = SupplyChainPartner.objects.get_or_create(
                id=uuid.uuid4(),
                defaults={
                    'name': f'{district} {random.choice(["Agro", "Farm", "Crop", "Green"])} {random.choice(["Store", "Depot", "Center", "Hub"])} {i+1}',
                    'partner_type': random.choice(partner_types),
                    'region': district,
                    'district': district,
                    'contact_person': f'Contact {i+1}',
                    'phone': f'+25670{random.randint(1000000, 9999999)}',
                    'email': f'partner{i+1}@example.com',
                    'latitude': lat + random.uniform(-0.1, 0.1),
                    'longitude': lng + random.uniform(-0.1, 0.1),
                    'status': 'active',
                    'company': company,
                }
            )
            partners.append(partner)
        
        self.stdout.write(f'Created {len(partners)} supply chain partners')
        
        feedback = []
        for vc in codes[:200]:
            fb, _ = ConsumerFeedback.objects.get_or_create(
                id=uuid.uuid4(),
                defaults={
                    'verification_code': vc,
                    'product': vc.batch.product,
                    'company': company,
                    'rating': random.randint(3, 5),
                    'comment': random.choice(['Great product!', 'Works well.', 'Satisfied with results.', 'Good quality.', '']),
                }
            )
            feedback.append(fb)
        
        self.stdout.write(f'Created {len(feedback)} feedback records')
        
        complaints = []
        for i in range(15):
            product = random.choice(products)
            complaint, _ = ProductReport.objects.get_or_create(
                id=uuid.uuid4(),
                defaults={
                    'product': product,
                    'company': company,
                    'reporter_name': f'Reporter {i+1}',
                    'reporter_email': f'reporter{i+1}@example.com',
                    'issue_type': random.choice(['Suspicious product', 'Damaged packaging', 'Wrong labeling', 'Expired product']),
                    'description': f'Description of complaint {i+1}',
                    'status': random.choice(['open', 'under_review', 'investigating', 'resolved']),
                    'priority': random.choice(['low', 'medium', 'high', 'critical']),
                }
            )
            complaints.append(complaint)
        
        self.stdout.write(f'Created {len(complaints)} complaints')
        
        insights = []
        for i in range(5):
            insight, _ = AiInsight.objects.get_or_create(
                id=uuid.uuid4(),
                defaults={
                    'category': random.choice(['fraud', 'verification', 'supply_chain', 'product']),
                    'title': f'Weekly Insight {i+1}',
                    'insight_text': f'Automated insight about {random.choice(["fraud trends", "verification patterns", "supply chain coverage", "product performance"])} for the week.',
                    'company': company,
                }
            )
            insights.append(insight)
        
        self.stdout.write(f'Created {len(insights)} AI insights')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded Bukoola Chemicals data!'))
        self.stdout.write(f'  Super Admin: admin@growsafe.com / SuperAdmin@2026')
        self.stdout.write(f'  Company Admin: admin@bukoola.com / Admin@2026')
        self.stdout.write(f'  Staff: staff@bukoola.com / Staff@2026')
