from .models import system_config as sys


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
