from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import core.utils as utils
from . import LegislativeYuan_ana
from . import president_ana
from app_advanced_search.sentiment_ana import sentiment_ana_main


def president_Lai(request):
    return render(request,
                  'app_special_ana/president_Lai.html')


def LegislativeYuan_caucus(request):
    return render(request,
                  'app_special_ana/LegislativeYuan_caucus.html')


def base(request):
    return render(request,
                  'app_special_ana/special_ana_base.html')


@csrf_exempt  # 取消 CSRF 保護
def president_data(request):
    if request.method == "POST":
        user_keywords: list = ["賴清德"]
        weeks: int = 4
        row_data = president_ana.ana_main(user_keywords, weeks)

        date, y = zip(*[(i["x"], int(i["y"])) for i in row_data['freqByDate']])
        BarValue = []
        BarCat = []
        for i in range(len(row_data["category"])):
            if row_data["freqByCate"][i] > 0:
                BarValue.append(row_data["freqByCate"][i])
                BarCat.append(row_data["category"][i])

        Response_data = {"date": list(date),
                         "y": list(y),
                         "BarValue": BarValue,
                         "BarCat": BarCat,
                         "num_occurrence": row_data["num_occurrence"],  # 總篇數
                         "num_frequency": row_data["num_frequency"],  # 總次數
                         "latest_news_time": utils.news_DBinfo()["latest_news_time"]
                         }

        return JsonResponse(Response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt  # 取消 CSRF 保護
def LegislativeYuan(request):
    if request.method == "POST":
        user_keywords: list = ["國民黨", "民進黨", "民眾黨"]
        weeks: int = 4
        Response_data = LegislativeYuan_ana.ana_main(user_keywords, weeks)
        Response_data["latest_news_time"] = utils.news_DBinfo()[
            "latest_news_time"]
        for word in user_keywords:
            Response_data["df_dict"][word]["sentiCount"] = sentiment_ana_main(
                word, "and", "全部", weeks)["sentiCount"]
        return JsonResponse(Response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)
