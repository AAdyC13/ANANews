from .models import system_config as sys


def news_categories() -> list[str]:
    """回傳 news_categories

    Returns:
        list[str]: news_categories
    """
    return sys.sysdb_get("news_categories")["news_categories"]


# def set_news_categories() -> bool:
#     """
#     設定 news_categories

#     Returns:
#         bool: 是否成功
#     """

#     data = {"news_categories": [
#         '要聞', '娛樂', '運動', '全球', '社會', '地方', '產經', '股市', '生活',
#         '文教', '評論', '兩岸', '科技', 'Oops', '旅遊',

#     ]}
#     # 只能及時列表處爬：娛樂 科技

#     return sys.sysdb_update("news_categories", data)