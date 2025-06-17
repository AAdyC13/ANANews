from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .predict_sentiment import predict_sentiment
from app_advanced_search.user_interest_ana import interest_ana_main
from app_advanced_search.sentiment_ana import sentiment_ana_main
from app_advanced_search.utils import filter_dataFrame
import json
import requests

url = "http://163.18.22.32:11435/api/generate"
# 設置遠程 Ollama 模型的基礎 URL
REMOTE_OLLAMA_URL = "http://163.18.22.32:11435"

model_name = "gemma3:4b"  # 默認模型名稱
# model_name = "qwen2.5:7b"  # 默認模型名稱
# model_name = "deepseek-r1:14b"  # 默認模型名稱
# 列出所有可用的模型
print(f"正在連接 {REMOTE_OLLAMA_URL} 檢查可用模型...")
response = requests.get(f"{REMOTE_OLLAMA_URL}/api/tags")
models = response.json()
print("\n可用的模型:")
available_models = [model['name'] for model in models['models']]
for model in available_models:
    print(f"- {model}")
# 檢查指定的模型是否可用
if model_name in available_models:
    print(f"\n✅ 模型 '{model_name}' 已可用")


def llm_report(request):
    return render(request,
                  'app_llm_report/llm_ollama.html')


def my_bert(request):
    return render(request,
                  'app_llm_report/my_bert.html')


def base(request):
    return render(request,
                  'app_llm_report/llm_base.html')


@csrf_exempt  # 取消 CSRF 保護
def my_bert_ana(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    data = json.loads(request.body)
    text: str = data.get("text")
    return JsonResponse({"data": predict_sentiment(text)})


def get_userkey_data(request):
    data = json.loads(request.body)
    userkey = data.get('user_keywords')
    cate = data.get('category', '')
    cond = data.get('cond', 'AND')
    weeks = data.get('weeks', 1)
    keys = userkey.split()

    df_query = filter_dataFrame(keys, cond, cate, weeks)

    # if df_query is empty, return an error message
    if len(df_query) == 0:
        return {'error': 'No results found for the given keywords.'}

    got_data = {}
    a = interest_ana_main(keys, cond, cate, weeks)
    got_data["newsCount"] = a[2]
    got_data["time_data"] = a[2]
    b = sentiment_ana_main(keys, cond, cate, weeks)
    got_data["sentiCount"] = b['sentiCount']
    got_data["data_pos"] = b['data_pos']
    got_data["data_neg"] = b['data_neg']

    return got_data


@csrf_exempt  # 取消 CSRF 保護
def ollama_request(request):
    if request.method == "POST":
        result = get_userkey_data(request)

        # Check if result is an error dictionary
        if isinstance(result, dict) and 'error' in result:
            return JsonResponse(result)

        userkey = request.POST.get('user_keywords') or "全部"
        key_occurrence_cat = result['newsCount']
        key_time_freq = result['time_data']

        sentiCount = result['sentiCount']
        line_data_pos = result['data_pos']
        line_data_neg = result['data_neg']

        # print(response1_data)
        # 系統提示指令
        system_prompt = f"以下是有關於[{userkey}]的網路聲量資訊，請做一份至少500字的詳細的專業分析報告。請使用繁體中文，並使用Markdown語法。"

        # 都出所有的輸入提示詞
        prompt = f'''{system_prompt}\n\n
    (1)聲量分析: 根據以下資料，幫我撰寫一份至少500字的詳細的專業分析報告
    以下是熱門程度，有多篇新聞報導提到:\n\n{key_occurrence_cat}\n\n
    以下是時間趨勢，這個關鍵字在過去幾天的報導數量變化:\n\n{key_time_freq}\n\n
    (2)情緒分析: 請根據以下資料，幫我撰寫一份至少500字的詳細的專業分析報告
    以下是情緒分析比率，正面負面的分布情況:\n\n{sentiCount}\n\n
    以下是情緒變化的時間趨勢，在過去幾天的報導情緒正負面的篇數數量變化:\n\n{line_data_pos}\n\n{line_data_neg}\n\n

    (3)分析的內容包括但不限於以下幾個方面：
    標題
    摘要
    關鍵字
    內容
    建議
    總結:
    '''

        # 這裡你可以呼叫ChatGPT的API來生成報告，或其他任何AI大型模型的API
        # 這裡使用requests來呼叫我用Ollama架設的遠端的API
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                url, json=payload, timeout=100)  # Add a timeout
            result = response.json()
            print(result['response'])
        except:
            print("Error:", response.status_code, response.text)
            return JsonResponse({'error': 'Failed to generate report. Please try again later.'})

        # 取得AI生成的報告
        response_report = {
            'report': result['response']
            # 'report': markdown.markdown(result['response'])
        }

        # Combine dictionaries correctly
        return JsonResponse(response_report)
    return JsonResponse({"error": "Invalid request"}, status=400)
