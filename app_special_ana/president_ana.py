import pandas as pd
from datetime import datetime, timedelta
from core.models import analysed_news as news
from core.utils import news_categories as newsCat
from typing import Any
import re

def ana_main(user_keywords, weeks) -> "dict[str, Any]":
    """
    依條件分析指定詞語，輸出供前端畫表格用的參數

    Args:
        user_keywords (_type_): 指定詞語
        cond (_type_): 過濾條件，and | or
        cate (_type_): 類別
        weeks (_type_): 從最新資料往回幾周

    Returns:
        dict: 供前端畫表格用的參數
    """
    global df
    df = news.db_get_all_DataFrame()
    df_query = filter_dataFrame(
        user_keywords, weeks)  # 回傳已過濾的dataFrame
    cate_freq, cate_occurrence = count_keyword(
        df_query, user_keywords)  # ,total_articles, total_frequency

    # 將Dataframe製作成用於點線圖顯示的xy軸
    date_samples = df_query.date
    query_freq = pd.DataFrame({'date_index': pd.to_datetime(
        date_samples), 'freq': [1 for _ in range(len(df_query))]})
    data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()
    line_xy_data = []
    for i, idx in enumerate(data.index):
        row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].freq)}
        line_xy_data.append(row)

    news_categories = ["全部"]+newsCat()
    freqByCate = [cate_occurrence[k] for k in news_categories]

    response = {'freqByDate': line_xy_data,  # 時間序列資料
                'freqByCate': freqByCate,  # 各類別的篇數
                'category': news_categories,  # 類別名稱
                'num_frequency': cate_freq['全部'],  # 這關鍵字被提多少次
                'num_occurrence': cate_occurrence['全部']  # 多少篇提到這關鍵字
                }
    return response


def filter_dataFrame(user_keywords, weeks):

    end_date, start_date = date_checker(weeks)

    # 期間條件
    period_condition = (df.date >= start_date) & (df.date <= end_date)

    # "全部"類別不必過濾新聞種類
    condition = period_condition

    # or條件
    # query keywords condition使用者輸入關鍵字條件
    condition = condition & df.content.apply(lambda text: any(
        (qk in text) for qk in user_keywords))  # 寫法:any()
    # condiction is a list of True or False boolean value
    df_query = df[condition]

    return df_query


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
