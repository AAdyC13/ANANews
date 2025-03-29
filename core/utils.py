from .models import system_config as sys
from .models import analysed_news as ana


def news_categories() -> list[str]:
    """回傳 news_categories

    Returns:
        list[str]: news_categories
    """
    return sys.sysdb_get("news_categories")["news_categories"]


def set_news_categories() -> bool:
    """
    設定 news_categories

    Returns:
        bool: 是否成功
    """

    data = {
        "news_categories": [
            '要聞', '社會', '地方', '全球', '兩岸',
            '產經', '股市', '運動', '生活', '文教'],
        "website_numbers": [1, 2, 3, 5, 4, 6, 11, 7, 9, 12]
    }

    return sys.sysdb_update("news_categories", data)


def news_DBinfo() -> dict:
    """回傳 news_DBinfo

    Returns:
        list[str]: news_DBinfo
    """
    return sys.sysdb_get("news_DBinfo")



# 預計是給爬蟲函數在結束時調用的
def set_news_DBinfo(latest_news_time: str) -> bool:
    """
    預計由爬蟲函數在結束時調用\n
    設定 news_DBinfo\n
    新聞收錄數量將自動更新
    Args:
        latest_news_time (str): 最新的新聞發布時間

    Returns:
        bool: 是否成功
    """

    data = {
        "latest_news_time": latest_news_time,
        "total_news": ana.objects.count()
    }

    return sys.sysdb_update("news_DBinfo", data)
