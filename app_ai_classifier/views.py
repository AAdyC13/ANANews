from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
from .custom_qwen_model import QwenForClassifier
from .openai import OpenAI

import uuid
import json
import torch
import torch.nn.functional as F

client = []

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dtype = torch.float16 if device.type == 'cuda' else torch.float32
sentiment_categories = ['負面', '正面']
sentimentlabel_to_id = {cate: i for i, cate in enumerate(sentiment_categories)}
id_to_sentimentlabel = {i: cate for i, cate in enumerate(sentiment_categories)}
news_categories = ['政治', '科技', '運動', '證卷',
                   '產經', '娛樂', '生活', '國際', '社會', '文化', '兩岸']
newslabel_to_id = {cate: i for i, cate in enumerate(news_categories)}
id_to_newslabel = {i: cate for i, cate in enumerate(news_categories)}
model_id = "Qwen/Qwen2.5-0.5B-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
full_model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
hidden_size = full_model.config.hidden_size
model_sentiment_classifier = QwenForClassifier(
    full_model.model, hidden_size, num_labels=len(sentiment_categories))
model_path_sentiment = "app_ai_classifier/trained_models/trained_sentiment_classifier_v4-5epochs-acc0.93"
model_sentiment_classifier.load_model(model_path_sentiment, device=device)
model_sentiment_classifier = model_sentiment_classifier.to(device)
# model_news_classifier = QwenForClassifier(
#     full_model.model, hidden_size, num_labels=len(news_categories))
# model_path_news = "app_llm_classifier/trained_models/trained_news_classifier_v3-6epochs-acc0.90"
# model_news_classifier.load_model(model_path_news, device=device)
# model_news_classifier = model_news_classifier.to(device)


def predict_sentiment(text):
    # Tokenize the input text
    inputs = tokenizer(
        text,
        max_length=512,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    # Get model predictions
    with torch.no_grad():
        outputs = model_sentiment_classifier(**inputs)

    # Extract logits and apply softmax to get probabilities
    logits = outputs["logits"]
    probabilities = F.softmax(logits, dim=-1)

    # Get the predicted class and label
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    predicted_label = id_to_sentimentlabel[predicted_class]

    # Get the confidence score
    confidence = probabilities[0][predicted_class].item()

    return {
        "text": text,
        "classification": predicted_label,
        "confidence": round(confidence, 2),
        "probabilities": {
            id_to_sentimentlabel[i]: round(prob.item(), 2) for i, prob in enumerate(probabilities[0])
        }
    }


def home_sentiment(request):
    return render(request, "app_ai_classifier/ai_sent.html")


def openai_talk(request):
    return render(request, "app_ai_classifier/openai_talk.html")


@csrf_exempt
def ai_connection(request):
    """
    處理 AI 連線請求
    """
    if request.method == "POST":
        data = json.loads(request.body)
        password = "123"  # data.get("password", "")
        if password != "123":
            return JsonResponse({"status": "error", "message": "You are not authorized to access this resource."}, status=403)
        if len(client) >= 5:
            return JsonResponse({"status": "error", "message": "Too many connections, please try again later."}, status=429)
        token = str(uuid.uuid4())
        client.append({"token": token, "times": 0})
        response = {
            "status": "success",
            "token": token,
        }
        return JsonResponse(response)

    return JsonResponse({"status": "error", "message": "Invalid request method123"}, status=400)


@csrf_exempt
def ai_talk(request):
    """
    處理 AI 對話請求
    """
    if request.method == "POST":
        data = json.loads(request.body)


        sentence = data.get("sentence", "")
        history = data.get("history", [])

        # 使用 OpenAI API 獲取 AI 回應
        try:
            ai_response = OpenAI.send_prompt(sentence, history)
            if not ai_response:
                ai_response = "抱歉，我無法理解您的問題。請嘗試使用其他方式表達您的問題。"
            response = {
                "status": "success",
                "message": ai_response,
            }
            return JsonResponse(response)
        except Exception as e:
            print(f"AI處理錯誤: {e}")
            return JsonResponse({"status": "error", "message": f"AI處理錯誤"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method444"}, status=400)


@csrf_exempt
def get_sentiment(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method656"}, status=400)
    input_text = json.loads(request.body).get('text')

    sentiment_prob = predict_sentiment(input_text)
    return JsonResponse(sentiment_prob)
