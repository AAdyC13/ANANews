from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .user_interest_ana import interest_ana_main
import json
from .assoc_ana import ana_main
from .sentiment_ana import ana_main


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


@csrf_exempt  # 取消 CSRF 保護
def get_user_interest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category: str = data.get("category")
        cond: str = data.get("cond")
        user_keywords: list = data.get("user_keywords").split(",")
        weeks: int = int(data.get("weeks"))
        row_data = interest_ana_main(
            user_keywords, cond, category, weeks)
        y, date = zip(*[(int(i["y"]), i["x"]) for i in row_data[0]])

        Response_data = {"y": list(y), "date": list(date),
                         "wordCount": list(row_data[1].values()), "newsCount": list(row_data[2].values())}
        return JsonResponse(Response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)

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