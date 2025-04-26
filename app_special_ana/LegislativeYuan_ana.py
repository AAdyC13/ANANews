import pandas as pd
from datetime import datetime, timedelta
from core.models import analysed_news as news
from core.utils import news_categories as newsCat
from typing import Any
from app_advanced_search.utils import filter_dataFrame_allCate
import re


def ana_main(user_keywords, weeks) -> "dict[str, Any]":
    """
    依條件分析指定詞語，輸出供前端畫表格用的參數

    Args:
        user_keywords (_type_): 指定詞語
        weeks (_type_): 從最新資料往回幾周

    Returns:
        dict: 供前端畫表格用的參數
    """
    df_dict = {}
    news_categories = ["全部"]+newsCat()

    for word in user_keywords:
        df_query = filter_dataFrame_allCate(word, "and", weeks)
        cate_freq, cate_occurrence = count_keyword(df_query, user_keywords)

        # 定義所有word的x軸(時間)和y軸(次數)
        date_samples = df_query.date
        query_freq = pd.DataFrame({'date_index': pd.to_datetime(
            date_samples), 'freq': [1 for _ in range(len(df_query))]})
        data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()
        line_xy_data = []
        for i, idx in enumerate(data.index):
            row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].freq)}
            line_xy_data.append(row)

        df_dict[word] = {
            'freqByDate': line_xy_data,  # 時間序列資料
            'num_frequency': cate_freq,  # 各類別的次數
            'num_occurrence': cate_occurrence,  # 各類別的篇數
        }

    response = {
        'category': news_categories,  # 類別名稱
        'df_dict': df_dict
    }
    return response


def count_keyword(df_query, query_keywords):
    news_categories = ["全部"]+newsCat()
    cate_occurrence = {}
    cate_freq = {}

    # 字典初始化
    for cate in news_categories:
        cate_occurrence[cate] = 0
        cate_freq[cate] = 0

    for idx, row in df_query.iterrows():
        # count the number of articles各類別篇數統計
        cate_occurrence[row.category] += 1
        cate_occurrence['全部'] += 1

        # count the keyword frequency各類別次數統計
        # 計算這一篇文章的content中重複含有多少個這些關鍵字(頻率)
        freq = sum([len(re.findall(keyword, row.content, re.I))
                   for keyword in query_keywords])
        cate_freq[row.category] += freq  # 在該新聞類別中累計頻率
        cate_freq['全部'] += freq  # 在"全部"類別中累計頻率

    # total_articles = cate_occurrence['全部']
    # total_frequency = cate_freq['全部']
    return cate_freq, cate_occurrence  # , total_articles, total_frequency
