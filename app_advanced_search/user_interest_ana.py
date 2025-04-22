import pandas as pd
from core.utils import news_categories as newsCat
from .utils import filter_dataFrame


def interest_ana_main(user_keywords, cond, cate, weeks):
    df_query = filter_dataFrame(
        user_keywords, cond, cate, weeks)  # 回傳已過濾的dataFrame

    # 將Dataframe製作成用於點線圖顯示的xy軸
    date_samples = df_query.date
    query_freq = pd.DataFrame({'date_index': pd.to_datetime(
        date_samples), 'freq': [1 for _ in range(len(df_query))]})
    data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()
    time_data = []
    for i, date_idx in enumerate(data.index):
        row = {'x': date_idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].freq)}
        time_data.append(row)

    wordCount, newsCount = count_keyword(
        user_keywords, df_query)

    return time_data, wordCount, newsCount


def count_keyword(user_keywords, df_query):
    news_categories = ["全部"]+newsCat()
    newsCount = {}
    wordCount = {}

    for cate in news_categories:
        newsCount[cate] = 0
        wordCount[cate] = 0

    for idx, row in df_query.iterrows():
        # count number of news
        newsCount[row.category] += 1
        newsCount['全部'] += 1

        # how manay times?
        freq = len([word for word in row.tokens_v2 if (word in user_keywords)])
        wordCount[row.category] += freq
        wordCount['全部'] += freq

    return wordCount, newsCount
