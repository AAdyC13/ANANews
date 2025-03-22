from django.shortcuts import render

def index(request):
    # context = {
    #         "top_keyword": "這是來自 Django 的變數"
    #     }
    return render(request, "index/index.html") #,context