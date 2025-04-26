from datetime import datetime, timedelta
from core.models import analysed_news as news


def filter_dataFrame(user_keywords, cond, cate, weeks):
    df = news.db_get_all_DataFrame()
    end_date: str = df.date.max()
    start_date = ""
    # start date
    try:
        start_date = (datetime.strptime(
            end_date, '%Y-%m-%d %H:%M').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"❗date_checker時間相減發生錯誤: {e}")

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


def filter_dataFrame_allCate(user_keywords, cond, weeks):
    df = news.db_get_all_DataFrame()
    end_date: str = df.date.max()
    start_date = ""
    # start date
    try:
        start_date = (datetime.strptime(
            end_date, '%Y-%m-%d %H:%M').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"❗date_checker時間相減發生錯誤: {e}")

    # 期間條件
    condition = (df.date >= start_date) & (df.date <= end_date)

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
