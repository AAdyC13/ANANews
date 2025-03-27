import pandas as pd
from datetime import datetime, timedelta
from core.models import analysed_news as news
from core.utils import news_categories as newsCat
# _cached_top_cate_person = None

df = news.db_get_all_DataFrame()


def ana_main(user_keywords, cond, cate, weeks):
    
    df_query = filter_dataFrame(user_keywords, cond, cate, weeks) # 回傳已過濾的dataFrame
    
    # 將Dataframe製作成用於點線圖顯示的xy軸
    date_samples = df_query.date
    query_freq = pd.DataFrame({'date_index': pd.to_datetime(
        date_samples), 'freq': [1 for _ in range(len(df_query))]})
    data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()
    time_data = []
    for i, date_idx in enumerate(data.index):
        row = {'x': date_idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].freq)}
        time_data.append(row)

    wordCount, newsCount = count_keyword(user_keywords, cond, weeks) # 回傳wordCount, newsCount兩個Dict

    return time_data, wordCount, newsCount


def filter_dataFrame(user_keywords, cond, cate, weeks):

    end_date, start_date = date_checker(weeks)

    # 期間條件
    period_condition = (df.date >= start_date) & (df.date <= end_date)

    # 新聞類別條件
    if (cate == "全部"):
        condition = period_condition  # "全部"類別不必過濾新聞種類
    else:
        # category新聞類別條件
        condition = period_condition & (df.category == cate)

    # and or 條件
    if (cond == 'and'):
        # query keywords condition使用者輸入關鍵字條件and
        condition = condition & df.content.apply(lambda text: all(
            (qk in text) for qk in user_keywords))  # 寫法:all()
    elif (cond == 'or'):
        # query keywords condition使用者輸入關鍵字條件
        condition = condition & df.content.apply(lambda text: any(
            (qk in text) for qk in user_keywords))  # 寫法:any()
    # condiction is a list of True or False boolean value
    df_query = df[condition]

    return df_query


def count_keyword(user_keywords, cond, weeks):
    end_date, start_date = date_checker(weeks)
    news_categories = ["全部"]+newsCat()
    newsCount = {}
    wordCount = {}
    if (cond == 'and'):
        query_df = df[
            (df.date >= start_date) & (df.date <= end_date)
            & df.tokens_v2.apply(lambda row: all((qk in row) for qk in user_keywords))
        ]
    elif (cond == 'or'):
        query_df = df[
            (df['date'] >= start_date) & (df['date'] <= end_date)
            & df.tokens_v2.apply(lambda row: any((qk in row) for qk in user_keywords))]

    for cate in news_categories:
        newsCount[cate] = 0
        wordCount[cate] = 0

    for idx, row in query_df.iterrows():
        # count number of news
        newsCount[row.category] += 1
        newsCount['全部'] += 1

        # how manay times?
        freq = len([word for word in row.tokens_v2 if (word in user_keywords)])
        wordCount[row.category] += freq
        wordCount['全部'] += freq

    return wordCount, newsCount


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
