from .models import analysed_news as news
from pandas import DataFrame
from datetime import datetime
from asgiref.sync import async_to_sync
import channels.layers
channel_layer = channels.layers.get_channel_layer()


def sentiment_analyzer():

    logs_Sender_Printer("🔥載入情緒分析模型")
    from transformers import BertTokenizer, BertForSequenceClassification

    # 中文情緒模型
    model_name = "uer/roberta-base-finetuned-jd-binary-chinese"
    # model_name = "bert-base-chinese"  # 官方中文

    # 載入模型與 tokenizer
    model = BertForSequenceClassification.from_pretrained(
        model_name, num_labels=2)
    # 自動選擇 GPU（如果可用）
    # device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
    device = 0
    model.to(device)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    logs_Sender_Printer("🔥載入情緒分析模型完成！")
    got_news_dict: DataFrame = news.db_get_sentiment_DataFrame()
    logs_Sender_Printer(f"ℹ️已讀取到{len(got_news_dict)}筆未分析新聞")
    logs_Sender_Printer(f"ℹ️開始進行情緒分析")

    def get_sentiment_proba_from_model(text) -> list:
        """
        分析文章情緒\n
        只能透過前512字分析，多餘部分會自動排除。

        Args:
            text (str): 欲分析文章

        Returns:
            list: [負面機率:float，正面機率:float]
        """
        max_length = 512  # 最多字數 若超出模型訓練時的字數，以模型最大字數為依據
        # prepare our text into tokenized sequence
        inputs = tokenizer(text, padding=True, truncation=True,
                           max_length=max_length, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        # perform inference to our model
        outputs = model(**inputs)
        # get output probabilities by doing softmax
        probs = outputs[0].softmax(1)

        response = [round(float(probs[0, 0]), 2), round(float(probs[0, 1]), 2)]
        # executing argmax function to get the candidate label
        # return probs.argmax()
        return response

    for idx, row in got_news_dict.iterrows():
        sentiment = get_sentiment_proba_from_model(
            row['content'])
        got_news_dict.at[idx, 'sentiment'] = sentiment  # 新增或更新 sentiment 欄位

    # 將 DataFrame 寫入資料庫
    if news.db_bulk_update_DataFrame(got_news_dict):
        logs_Sender_Printer("✅已儲存情緒分析")
    else:
        logs_Sender_Printer("❗情緒分析儲存失敗")


def logs_Sender_Printer(message: str) -> bool:
    """
    向asgi伺服器發送WebSocket訊息

    Args:
        message (str): 要發送的訊息

    Returns:
        bool: 是否成功
    """
    try:
        print(message)
        log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [sentiment_analyzer] {message}"
        async_to_sync(channel_layer.group_send)(
            "celery_logs", {"type": "log_message", "message": log_message}
        )
        return True
    except Exception as ex:
        print(f"❗core/sentiment_analyzer/logs_sender 錯誤: {ex}")
        return False
