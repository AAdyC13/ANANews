import pandas as pd
from core.models import analysed_news as news
from .utils import filter_dataFrame


def sentiment_ana_main(user_keywords, cond, cate, weeks):
    df_query = filter_dataFrame(
        user_keywords, cond, cate, weeks)  # 回傳已過濾的dataFrame

    sentiCount, sentiPercnt = get_article_sentiment(df_query)

    if weeks <= 4:
        freq_type = 'D'
    else:
        freq_type = 'W'

    line_data_pos = get_daily_basis_sentiment_count(
        df_query, sentiment_type='pos', freq_type=freq_type)
    line_data_neg = get_daily_basis_sentiment_count(
        df_query, sentiment_type='neg', freq_type=freq_type)

    response = {
        'sentiCount': sentiCount,
        'data_pos': line_data_pos,
        'data_neg': line_data_neg,
    }
    return response


def get_article_sentiment(df_query):
    sentiCount = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    sentiPercnt = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    numberOfArticle = len(df_query)
    for senti in df_query.sentiment:
        # determine sentimental polarity
        if float(senti[1]) >= 0.8:
            sentiCount['Positive'] += 1
        elif float(senti[1]) <= 0.7:
            sentiCount['Negative'] += 1
        else:
            sentiCount['Neutral'] += 1
    for polar in sentiCount:
        try:
            sentiPercnt[polar] = int(sentiCount[polar]/numberOfArticle*100)
        except:
            sentiPercnt[polar] = 0  # 若分母 numberOfArticle=0會報錯
    return sentiCount, sentiPercnt


def get_daily_basis_sentiment_count(df_query, sentiment_type='pos', freq_type='D'):

    # 自訂正負向中立的標準，sentiment score是機率值，介於0~1之間
    # Using lambda to determine if an article is postive or not.
    if sentiment_type == 'pos':
        def lambda_function(
            senti): return 1 if senti >= 0.75 else 0  # 大於0.75為正向
    elif sentiment_type == 'neg':
        def lambda_function(senti): return 1 if senti <= 0.7 else 0  # 小於0.7為負向
    elif sentiment_type == 'neutral':
        def lambda_function(
            senti): return 1 if senti > 0.75 & senti < 0.7 else 0  # 介於中間為中立
    else:
        return None

    freq_df = pd.DataFrame({'date_index': pd.to_datetime(df_query.date),
                            'frequency': [lambda_function(senti[1]) for senti in df_query.sentiment]})
    # Group rows by the date to the daily number of articles. 加總合併同一天新聞，篇數就被計算好了
    freq_df_group = freq_df.groupby(pd.Grouper(
        key='date_index', freq=freq_type)).sum()

    # 'date_index'為index(索引)，將其變成欄位名稱，inplace=True表示原始檔案會被異動
    freq_df_group.reset_index(inplace=True)

    # x,y，用於畫趨勢線圖
    xy_line_data = [{'x': date.strftime('%Y-%m-%d'), 'y': freq}
                    for date, freq in zip(freq_df_group.date_index, freq_df_group.frequency)]
    return xy_line_data
