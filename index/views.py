from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from core.utils import news_DBinfo, set_news_DBinfo
from datetime import datetime


def index(request):
    return render(request, "index/index.html")


@csrf_exempt  # 取消 CSRF 保護
def get_news_DBinfo(request):
    # set_news_DBinfo("還沒做完")
    data = news_DBinfo()
    return JsonResponse({"latest_news_time": data["latest_news_time"], "total_news": data["total_news"]})


@csrf_exempt  # 取消 CSRF 保護
def news_scraper_start(request):
    from core.tasks import do_thing
    a = do_thing.delay("檢查詞")
    print(a.id)
    return JsonResponse({"hi":"11"})