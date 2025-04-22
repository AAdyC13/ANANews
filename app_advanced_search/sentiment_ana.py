from core.models import analysed_news as news
from .utils import filter_dataFrame


def ana_main(user_keywords, cond, cate, weeks):
    df_query = filter_dataFrame(
        user_keywords, cond, cate, weeks)  # 回傳已過濾的dataFrame

    return {
    }
