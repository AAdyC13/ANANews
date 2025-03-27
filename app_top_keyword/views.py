from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import app_top_keyword.top_keyword_ana as keyword_ana
import app_top_keyword.top_person_ana as person_ana
import app_top_keyword.user_interest_ana as interest_ana
from core.utils import news_categories as newsCat


def top_keyword(request):
    return render(request,
                  'app_top_keyword/top_keyword.html')


def top_person(request):
    return render(request,
                  'app_top_keyword/top_person.html')


def base(request):
    return render(request,
                  'app_top_keyword/top_base.html')


def user_interest(request):
    return render(request,
                  'app_top_keyword/user_interest.html')


@csrf_exempt  # 取消 CSRF 保護
def get_chart_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        keyword_max = int(data.get("keyword_count"))
        category: str = data.get("category")

        ana = keyword_ana.top_keyword_ana(category)

        label = []
        dataset = []
        for each_word in ana[:keyword_max]:
            label.append(each_word[0])
            dataset.append(each_word[1])
        Response_data = {"words": label, "counts": dataset}

        return JsonResponse(Response_data)
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt  # 取消 CSRF 保護
def get_persons(request):
    if request.method == "POST":
        data = json.loads(request.body)
        keyword_max = int(data.get("person_count"))
        category: str = data.get("category")

        ana = person_ana.top_keyword_ana(category)

        label = []
        dataset = []
        for each_word in ana[:keyword_max]:
            label.append(each_word[0])
            dataset.append(each_word[1])
        Response_data = {"words": label, "counts": dataset}
        return JsonResponse(Response_data)
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt  # 取消 CSRF 保護
def get_categories(request):
    categories = ["全部"]
    categories += newsCat()
    return JsonResponse({"categories": categories})


@csrf_exempt  # 取消 CSRF 保護
def get_user_interest(request):
    if request.method == "POST":
        data = json.loads(request.body)

        category: str = data.get("category")
        cond: str = data.get("cond")
        user_keywords: list = data.get("user_keywords").split(",")
        weeks: int = int(data.get("weeks"))
        row_data = interest_ana.ana_main(
            user_keywords, cond, category, weeks)
        y, date = zip(*[(int(i["y"]), i["x"]) for i in row_data[0]])

        Response_data = {"y": list(y), "date": list(date),
                         "wordCount": list(row_data[1].values()), "newsCount": list(row_data[2].values())}
        return JsonResponse(Response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)
