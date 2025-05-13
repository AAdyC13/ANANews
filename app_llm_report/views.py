from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def llm_report(request):
    return render(request,
                  'app_llm_report/llm_report.html')


def base(request):
    return render(request,
                  'app_llm_report/base.html')
