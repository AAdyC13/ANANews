from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import app_top_keyword.top_keyword_ana as tops

def home(request):
    return render(request,
                      'app_top_keyword/app_top_keyword.html')

@csrf_exempt  # 取消 CSRF 保護
def get_chart_data(request):
    if request.method == "POST":
        data = json.loads(request.body)  
        keyword_max = int(data.get("keyword_count"))
        category:str = data.get("category")

        keyword_ana = tops.top_keyword_ana(category)
 
        label = []
        dataset = []
        for each_word in keyword_ana[:keyword_max]:
            label.append(each_word[0])
            dataset.append(each_word[1])
        Response_data= {"words": label, "counts": dataset}
                  
        return JsonResponse(Response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)