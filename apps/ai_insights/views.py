from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AiInsight

@login_required
def insights_list(request):
    insights = AiInsight.objects.all()[:20]
    return render(request, 'dashboard/ai_insights/list.html', {'insights': insights})

@login_required
def query_insights(request):
    query = request.GET.get('q', '')
    
    from .services import AiQueryService
    result = AiQueryService().process_query(query, request.company)
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({'success': True, 'data': result})
    
    return render(request, 'dashboard/ai_insights/query_result.html', {'result': result, 'query': query})
