from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def president_Lai(request):
    return render(request,
                  'app_special_ana/president_Lai.html')


def base(request):
    return render(request,
                  'app_special_ana/special_ana_base.html')
