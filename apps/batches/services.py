from datetime import datetime

class BatchNumberGenerator:
    def generate(self, batch):
        company_prefix = batch.company.slug[:3].upper()
        year = batch.manufacture_date.year
        sequence = batch.product.batches.filter(manufacture_date__year=year).count() + 1
        return f"{company_prefix}-{year}-{sequence:04d}"
