from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django_ratelimit.decorators import ratelimit
from .services import VerificationService
from .tasks import log_scan_event

@require_GET
@ratelimit(key='ip', rate='30/m', block=True)
def verify_code(request, code):
    context = {
        'ip_address': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'channel': 'web',
    }
    
    result = VerificationService().verify(code, context)
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'data': {
                'result': result['result'],
                'product': result['product_data'] if result.get('product_data') else None,
            }
        })
    
    return render(request, 'verify/result.html', result)

@require_POST
@ratelimit(key='ip', rate='30/m', block=True)
def submit_feedback(request):
    code = request.POST.get('code')
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '')
    
    from apps.feedback.models import ConsumerFeedback
    from apps.verification.models import VerificationCode
    
    vcode = VerificationCode.objects.filter(code=code).first()
    if vcode:
        ConsumerFeedback.objects.create(
            verification_code=vcode,
            product=vcode.batch.product,
            company=vcode.company,
            rating=rating,
            comment=comment,
        )
    
    return JsonResponse({'success': True})
