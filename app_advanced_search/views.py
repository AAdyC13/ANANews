from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from .assoc_ana import ana_main


def base(request):
    return render(request,
                  'app_advanced_search/adv_base.html')


def user_interest(request):
    return render(request,
                  'app_advanced_search/user_interest.html')


def keyword_assoc(request):
    return render(request,
                  'app_advanced_search/keyword_assoc.html')


def sentiment(request):
    return render(request,
                  'app_advanced_search/sentiment.html')


@csrf_exempt
def assoc_ana(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category: str = data.get("category")
        cond: str = data.get("cond")
        user_keywords: list = data.get("user_keywords").split(",")
        weeks: int = int(data.get("weeks"))
        row_data = ana_main(
            user_keywords, cond, category, weeks)
        return JsonResponse(row_data)
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def sentiment_ana(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category: str = data.get("category")
        cond: str = data.get("cond")
        user_keywords: list = data.get("user_keywords").split(",")
        weeks: int = int(data.get("weeks"))
        # row_data = sentiment_main(
        #     user_keywords, cond, category, weeks)
        # print(row_data)
        return JsonResponse()
    return JsonResponse({"error": "Invalid request"}, status=400)
