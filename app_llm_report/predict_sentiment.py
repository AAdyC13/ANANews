from transformers import AutoTokenizer, pipeline, BertForSequenceClassification
import torch

# Setting device on GPU if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# (2) or Load model from local
best_model = "app_llm_report\\my_bert_sentimentANA_model"  #
# model = AutoModelForSequenceClassification.from_pretrained("./my-best-model").to(device)
model = BertForSequenceClassification.from_pretrained(
    best_model, num_labels=2).to(device)  # specify number of labels
tokenizer = AutoTokenizer.from_pretrained(best_model)
categories = ['負面', '正面']
id_to_label = {i: cate for i, cate in enumerate(categories)}

# model, tokenizer, device


def predict_sentiment(text):
    max_length = 512  # 最多字數 若超出模型訓練時的字數，以模型最大字數為依據
    # Tokenize the input text
    inputs = tokenizer(
        text,
        max_length=max_length,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract logits and apply softmax to get probabilities
    # logits = outputs.logits
    logits = outputs["logits"]  # 取出 logits

    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # Get the predicted class (0: negative, 1: positive)
    predicted_class = torch.argmax(probabilities, dim=-1).item()

    # Get the class name using id_to_label
    predicted_label = id_to_label[predicted_class]

    # Get the confidence score
    confidence = probabilities[0][predicted_class].item()

    return {
        # "text": text,
        "預測結果": predicted_label,
        "判斷信心": f"{round(confidence * 100, 2)} %",
        "正面情緒": f"{round(probabilities[0][1].item() * 100, 2)} %",
        "負面情緒": f"{round(probabilities[0][0].item() * 100, 2)} %"
    }
