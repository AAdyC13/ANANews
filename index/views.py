from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import core.utils as utils
import core.tasks as tasks
import core.news_scraper as news_scraper
from datetime import datetime


def index(request):
    return render(request, "index/index.html")


def web_intro(request):
    return render(request, "index/me.html")


@csrf_exempt  # 取消 CSRF 保護
def get_news_DBinfo(request):
    # set_news_DBinfo("還沒做完")
    data = utils.news_DBinfo()
    return JsonResponse({"latest_news_time": data["latest_news_time"], "total_news": data["total_news"]})


@csrf_exempt  # 取消 CSRF 保護
def task_test(request):
    try:
        a = tasks.test.delay("測試")
        word = f"✅成功發布任務：{a.id}"
        print(word)
        return JsonResponse({"Response": word})
    except Exception as ex:
        word = f"❗發布任務失敗：{ex}"
        print(word)
        return JsonResponse({"Response": word})


@csrf_exempt  # 取消 CSRF 保護
def news_scraper_start(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            a = news_scraper.news_scraper_starter.delay(
                data.get("categorys"), int(data.get("each_Num")),)
            word = f"✅成功發布任務：{a.id}"
            print(word)
            return JsonResponse({"Response": word})
        except Exception as ex:
            word = f"❗發布任務失敗：{ex}"
            print(word)
            return JsonResponse({"Response": word})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt  # 取消 CSRF 保護
def check_scraper_isWork(request):
    return JsonResponse({"Response": utils.news_scraper_isWork()})
