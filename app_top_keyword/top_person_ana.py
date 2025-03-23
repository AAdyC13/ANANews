from collections import Counter
from core.models import analysed_news as news
from core.utils import news_categories as newsCat
_cached_top_cate_person = None


def analyze_top_person():
    def NerToken(word, ner, idx):
        return ner,word
    df = news.db_get_all_DataFrame()
    news_categories = newsCat()
    allowedNE=['PERSON']
    counter_all = Counter()
    top_cate_person = {}
    
    for category in news_categories:
        df_group = df[df.category == category]
        words_group = []

        for row in df_group.entities:
            filtered_words = [word for ner, word in eval(
                row) if len(word) >= 2 and ner in allowedNE]
            words_group += filtered_words

        counter = Counter(words_group)
        counter_all += counter
        top_cate_person[category] = counter.most_common(200)
    
    top_cate_person['全部'] = counter_all.most_common(200)
    return top_cate_person

def top_keyword_ana(category: str) -> dict:
    """
    回傳聯合新聞網所有類別的人物及其數量

    Args:
        category (str): 類別

    Returns:
        dict: 關鍵字及其數量
    """
    global _cached_top_cate_person  # 使用全域變數來快取結果
    if _cached_top_cate_person is None:
        _cached_top_cate_person = analyze_top_person()  # 只在程式啟動時計算一次
    return _cached_top_cate_person.get(category, {})  # 回傳對應類別的結果