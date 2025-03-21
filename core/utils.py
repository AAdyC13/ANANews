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

    data = {"news_categories": [
        '要聞', '娛樂', '運動', '全球', '社會', '地方', '產經', '股市', '房市', '生活', '寵物',
        '健康', '橘世代', '文教', '評論', '兩岸', '科技', 'Oops', '閱讀', '旅遊', '雜誌', '報時光',
        '倡議+', '500輯', '轉角國際', 'NBA', '時尚', '汽車', '棒球', 'HBL', '遊戲', '專題', '網誌', '女子漾'
    ]}
    return sys.sysdb_update("news_categories", data)

#print(set_news_categories())