import pandas as pd
from datetime import datetime, timedelta
from core.models import analysed_news as news
from collections import Counter
import re


def ana_main(user_keywords, cond, cate, weeks):
    global df
    df = news.db_get_all_DataFrame()
    df_query = filter_dataFrame(
        user_keywords, cond, cate, weeks)  # 回傳已過濾的dataFrame

    # if df_query is empty, return an error message
    if len(df_query) == 0:
        return None

    newslinks = get_title_link_topk(df_query, k=15)
    related_words, clouddata = get_related_word_clouddata(df_query)
    same_paragraph = get_same_para(
        df_query, user_keywords, cond, k=10)  # multiple keywords

    return {
        'newslinks': newslinks,
        'related_words': related_words,
        'same_paragraph': same_paragraph,
        'clouddata': clouddata,
        'num_articles': len(df_query),
    }


def filter_dataFrame(user_keywords, cond, cate, weeks):

    end_date, start_date = date_checker(weeks)

    # 新聞類別條件
    if (cate == "全部") & (cond == 'and'):
        df_query = df[(df.date >= start_date) & (df.date <= end_date)
                      & df.content.apply(lambda text: all((qk in text) for qk in user_keywords))]
    elif (cate == "全部") & (cond == 'or'):
        df_query = df[(df['date'] >= start_date) & (df['date'] <= end_date)
                      & df.content.apply(lambda text: any((qk in text) for qk in user_keywords))]
    elif (cond == 'and'):
        df_query = df[(df.category == cate)
                      & (df.date >= start_date) & (df.date <= end_date)
                      & df.content.apply(lambda text: all((qk in text) for qk in user_keywords))]
    elif (cond == 'or'):
        df_query = df[(df.category == cate)
                      & (df['date'] >= start_date) & (df['date'] <= end_date)
                      & df.content.apply(lambda text: any((qk in text) for qk in user_keywords))]

    return df_query


def get_title_link_topk(df_query, k=5) -> list:
    """
    回傳df內的前k個「類別」「標題」「連結」「圖片」

    Args:
        df_query
        k (int): 前多少個新聞。默認為5。

    Returns:
        list
    """
    items = []
    for i in range(len(df_query[0:k])):  # show only 5 articles
        category = df_query.iloc[i]['category']
        title = df_query.iloc[i]['title']

        link = news.db_object_get((df_query.iloc[i]["news_id_one"],
                                  df_query.iloc[i]["news_id_two"])).news_url_get()
        photo_link = df_query.iloc[i]['photo_link']
        # if photo_link value is NaN, replace it with empty string
        if pd.isna(photo_link):
            photo_link = ''  # 若沒圖片，就設定為空字串，在前端網頁解讀json格式時才不會錯誤

        item_info = {
            'category': category,
            'title': title,
            'link': link,
            'photo_link': photo_link
        }

        items.append(item_info)
    return items


def get_related_words(df_query) -> list:
    """
    相關詞有哪一些?找出各篇文章的topk關鍵詞加以彙整計算。\n
    不能用 "get_related_keys"當函數名稱，因為這是Django系統用的名稱。

    Args:
        df_query

    Returns:
        list: 前30筆最相關詞
    """
    counter = Counter()  # this counter is for all articles
    for idx in range(len(df_query)):
        pair_list = df_query.iloc[idx].top_key_freq  # 已經是 list，不需要 eval
        counter += Counter(dict(pair_list))
    return counter.most_common(30)  # return list format


def get_related_word_clouddata(df_query) -> "list| list[dict[str, any]]":
    """
    Get related keywords by counting the top keywords of each news.\n
    Notice:  do not name function as  "get_related_keys",\n
    because this name is used in Django

    Args:
        df_query

    Returns:
        list:前20筆最相關詞
        list[dict[text:str, size:int]]: 文字雲data
    """
    # (1) Get wf_pairs by calling get_related_words().
    wf_pairs = get_related_words(df_query)

    # (2) cloud chart data
    # the minimum and maximum frequency of top words
    min_ = wf_pairs[-1][1]  # the last line is smaller
    max_ = wf_pairs[0][1]
    # text size based on the value of word frequency for drawing cloud chart
    # Scaling frequency value into an interval of from 20 to 120.
    textSizeMin = 20  # 最小字
    textSizeMax = 120  # 最大字

    # if all frequences are the same, "divided by zero" exception will arise.
    # In the following case, exception will arise.
    # We must deal with this.
    # [('AA', 1), ('BB', 1), ('CC', 1)]
    # Instead of (max_-min_), we use len(wf_pairs) as divisor.
    # every word size is 1 / len(wf_pairs)
    # 當每個字的頻率都一樣時，讓每個字的高度大小都一樣，分子是1，分母是字數==>均分

    # 排除分母為0的情況
    # 這裡的min_是最小值，max_是最大值，這兩個值是頻率的大小
    if (min_ != max_):
        max_min_range = max_ - min_

    else:
        max_min_range = len(wf_pairs)  # 關鍵詞的數量: 20個
        min_ = min_ - 1  # every size is 1 / len(wf_pairs)

    # word cloud chart data using proportional scaling
    # 排除分母為0的情況
    clouddata = [{'text': w, 'size': int(
        textSizeMin + (f - min_)/max_min_range * (textSizeMax-textSizeMin))} for w, f in wf_pairs]

    # 可能分母為0的情況
    # clouddata = [{'text': w, 'size': int(textSizeMin + (f - min_) / (max_ - min_) * (textSizeMax - textSizeMin))} for w, f in wf_pairs]

    return wf_pairs, clouddata


def cut_paragraph(text):
    paragraphs = text.split('。')  # 遇到句號就切開 功能有限
    # paragraphs = re.split('。', text) # 遇到句號就切開
    # paragraphs = re.split('[。！!？?]', text) # 遇到句號(也納入問號、驚嘆號、分號等)就切開
    paragraphs = list(filter(None, paragraphs))
    return paragraphs


def get_same_para(df_query, user_keywords, cond, k=10) -> list:
    """
    Find out all paragraphs where multiple keywords occur.

    Returns:
        list: 最相關的幾份內文
    """
    same_para = []
    for text in df_query.content:
        # print(text)
        paragraphs = cut_paragraph(text)
        for para in paragraphs:
            para += "。"  # 在每段落文字後面加一個句號。
            # 判斷每個段落文字是否包含該關鍵字，and or分開判斷
            if cond == 'and':
                if all([kw in para for kw in user_keywords]):
                    same_para.append(para)  # 符合條件的段落para保存起來
            elif cond == 'or':
                if any([kw in para for kw in user_keywords]):
                    same_para.append(para)  # 符合條件的段落para保存起來
    return same_para[0:k]


def date_checker(weeks: int):
    end_date: str = df.date.max()
    start_date = ""
    # start date
    try:
        start_date = (datetime.strptime(
            end_date, '%Y-%m-%d %H:%M').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
        return end_date, start_date
    except Exception as e:
        print(f"❗app_top_keyword/user_interest_ana/時間相減發生錯誤: {e}")
        return end_date, start_date
