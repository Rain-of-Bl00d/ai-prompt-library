import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Prompt

@csrf_exempt
def prompt_list_create(request):
    """
    Handles GET /prompts/ (List) and POST /prompts/ (Create)
    """
    if request.method == 'GET':
        prompts = list(Prompt.objects.all().values('id', 'title', 'content', 'complexity', 'created_at'))
        # Convert datetime to ISO string for JSON serialization
        for p in prompts:
            if p.get('created_at'):
                p['created_at'] = p['created_at'].isoformat()
        return JsonResponse(prompts, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = Prompt.objects.create(
                title=data.get('title'),
                content=data.get('content'),
                complexity=data.get('complexity')
            )
            return JsonResponse({
                'id': prompt.id,
                'title': prompt.title
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def prompt_detail(request, pk):
    """
    Handles GET /prompts/:id/ (Retrieve + Redis View Counter)
    """
    prompt = get_object_or_404(Prompt, pk=pk)

    # Redis Integration: Increment view count
    redis_key = f"prompt_views_{pk}"

    try:
        view_count = cache.incr(redis_key)
    except (ValueError, Exception):
        cache.set(redis_key, 1)
        view_count = 1

    return JsonResponse({
        'id': prompt.id,
        'title': prompt.title,
        'content': prompt.content,
        'complexity': prompt.complexity,
        'view_count': view_count,
        'created_at': prompt.created_at.isoformat(),
    })