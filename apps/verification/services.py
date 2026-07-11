import secrets
from django.utils import timezone
from .models import VerificationCode, ScanEvent

class CodeGenerationService:
    ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    
    def generate_code(self, company_prefix, year):
        while True:
            payload = self._random_payload(8)
            code = f"{company_prefix}-{year}-{payload}"
            check_digit = self._luhn_check_digit(code)
            full_code = f"{code}-{check_digit}"
            if not VerificationCode.objects.filter(code=full_code).exists():
                return full_code
    
    def _random_payload(self, length):
        return "".join(secrets.choice(self.ALPHABET) for _ in range(length))
    
    def _luhn_check_digit(self, value):
        total = 0
        alternate = False
        for ch in reversed(value):
            n = ord(ch)
            if alternate:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
            alternate = not alternate
        return (10 - (total % 10)) % 10
    
    def generate_bulk(self, batch, quantity):
        company_prefix = batch.company.slug[:3].upper()
        year = batch.manufacture_date.year
        codes = []
        for _ in range(quantity):
            code_str = self.generate_code(company_prefix, year)
            codes.append(VerificationCode(
                code=code_str,
                batch=batch,
                company=batch.company,
            ))
        return codes

class VerificationService:
    def verify(self, code, context):
        vcode = VerificationCode.objects.select_related(
            'batch__product', 'batch__company'
        ).filter(code=code).first()
        
        if not vcode:
            result = 'invalid'
            product_data = None
        elif vcode.batch.status == 'recalled':
            result = 'recalled'
            product_data = self._get_product_data(vcode)
        elif vcode.batch.expiry_date and vcode.batch.expiry_date < timezone.now().date():
            result = 'expired'
            product_data = self._get_product_data(vcode)
        elif vcode.scan_count == 0:
            result = 'genuine'
            product_data = self._get_product_data(vcode)
        else:
            result = 'already_used'
            product_data = self._get_product_data(vcode)
        
        if vcode:
            vcode.scan_count += 1
            if result == 'genuine':
                vcode.first_scanned_at = timezone.now()
            vcode.last_scanned_at = timezone.now()
            vcode.save(update_fields=['scan_count', 'first_scanned_at', 'last_scanned_at'])
        
        log_scan_event.delay(code, vcode.id if vcode else None, 
                           vcode.company_id if vcode else None, result, context)
        
        return {
            'result': result,
            'verification_code': vcode,
            'product_data': product_data,
        }
    
    def _get_product_data(self, vcode):
        return {
            'name': vcode.batch.product.name,
            'company': vcode.batch.company.name,
            'batch': vcode.batch.batch_number,
            'manufacture_date': vcode.batch.manufacture_date,
            'expiry_date': vcode.batch.expiry_date,
        }
