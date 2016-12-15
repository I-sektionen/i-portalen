from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Result


def liu_crawler(request):
    return render(request, 'liu_crawler/liu_crawler.html')


@csrf_exempt
def add_result(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            score = request.POST.get('score')
            Result(name=name, score=score).save()
            return JsonResponse({'success': True})
        except:
            pass
    return JsonResponse({'success': False})


@csrf_exempt
def get_result(request):
    return HttpResponse(serializers.serialize("json", Result.objects.all().order_by('-score')[0:10]), content_type='application/json')
