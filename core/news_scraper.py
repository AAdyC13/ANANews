from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from .models import analysed_news as news
from .models import system_config as sysdb
import time
from datetime import datetime, timedelta
from celery import shared_task
import channels.layers
from asgiref.sync import async_to_sync
channel_layer = channels.layers.get_channel_layer()

user_agent = UserAgent()


@shared_task
def news_scraper_starter(want_category: list, each_num: int) -> bool:
    """
    celery函數\n
    從【聯合新聞網】的【即時】頁面底下\n
    抓取及時列表中【要聞】,【社會】,【地方】,【全球】,【兩岸】,\n
    【產經】,【股市】,【運動】,【生活】,【文教】\n
    類新聞(數量因各種情況受影響)並存入資料庫
    Args:
        want_category (list): 要爬取的類別
        each_num (int): 各類別要爬取的新聞數量
    Returns:
        bool: 是否成功
    """
    def news_collector() -> bool:
        """
        主程序，呼叫單爬蟲逐一爬取，太多request會被封

        Returns:
            bool: 是否成功
        """
        news_counter = 0
        for i in range(len(want_category)):
            logs_Sender_Printer(f"開始爬取【{want_category[i]}】類新聞")
            if each_num == 0:
                time.sleep(0.1)
            else:
                inside_counter = 0
                page = web_requester(
                    f"https://udn.com/news/breaknews/1/{want_category[i]}#breaknews")
                if (page):
                    for each_news in page.find_all('a', {"class": "story-list__image--holder", 'data-content_level': "開放閱讀"}):
                        if inside_counter >= each_num:
                            break
                        inside_counter += 1
                        news_dict = {}
                        if each_news.get('href'):
                            parts = each_news.get('href').split("/")
                            news_id1, news_id2 = parts[-2], parts[-1].split("?")[0]
                            news_id = (int(news_id1), int(news_id2))
                            if news.db_is_news_exists(news_id):
                                logs_Sender_Printer(f"🔸已收錄新聞：{news_id}")
                            else:
                                data = news_story_extract(each_news.get('href'))
                                if data:
                                    news_dict = {
                                        "title": each_news.get('aria-label'),
                                        "photo_link": each_news.find('source', {"type": "image/webp"}).get('srcset').replace("&", "&amp;")
                                    } | data

                                    if news.db_update(news_id, news_dict):
                                        logs_Sender_Printer(f"新收錄新聞：{news_id}")
                                        news_counter += 1
                                    else:
                                        logs_Sender_Printer(f"❗收錄新聞失敗：{news_id}")
                                else:
                                    logs_Sender_Printer(f"❗收錄新聞失敗：{news_id}")

        logs_Sender_Printer(f"✅本次一共新收錄{news_counter}份新聞")

    def web_requester(url: str) -> BeautifulSoup | None:
        """
        爬蟲函數
        Args:
            url (str): 網頁連結
        Returns:
            BeautifulSoup|None: 爬取內容，若失敗回傳None

        """
        try:
            req = requests.get(
                url, headers={'user-agent': user_agent.random}, timeout=10)
            req.raise_for_status()  # 如果返回狀態碼不正常，則會觸發異常
            time.sleep(10)  # 所有網站呼叫的操作必須休息10秒再進行下一次爬取
            return BeautifulSoup(req.text, 'lxml')

        except requests.exceptions.RequestException as e:
            logs_Sender_Printer(f"❗core/news_scraper/web_requester 爬取失敗: {e}")
            return None

    def news_story_extract(news_link: str) -> dict | None:
        """
        負責爬取新聞內文

        Args:
            news_link (str): 內文鏈接

        Returns:
            dict | None: 回傳整理好的內文，若無回傳None
        """
        in_page = web_requester("https://udn.com"+news_link)
        if in_page:
            # 重要：replace("&", "&amp;")是必要的，網站伺服器會針對 & 和 &amp 傳輸兩張不一樣的圖片，據觀察，好像是大圖和縮小圖，縮小圖應該是為了不占用資源的版本
            try:
                return {
                    "date": in_page.find('div', {"class": "article-content__subinfo"}).find('section', {"class": "authors"}).find('time', {"class": "article-content__time"}).get_text('', strip=True),
                    "category": in_page.find('nav', {"class": "article-content__breadcrumb"}).find_all("a")[1].get_text('', strip=True),
                    "content": in_page.find('section', {"class": "article-content__editor"}).get_text('', strip=True),
                }
            except AttributeError as e:
                logs_Sender_Printer(
                    f"❗core/news_scraper/news_story_extract 找不到對應資料: {e}")
                return None
            except IndexError as e:
                logs_Sender_Printer(
                    f"❗core/news_scraper/news_story_extract 內文category的find_all('a')[1]出錯: {e}")
                return None

    def logs_Sender_Printer(message: str) -> bool:
        """
        向asgi伺服器發送WebSocket訊息

        Args:
            message (str): 要發送的訊息

        Returns:
            bool: 是否成功
        """
        try:
            print(message)
            log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [news_scraper] {message}"
            async_to_sync(channel_layer.group_send)(
                "celery_logs", {"type": "log_message", "message": log_message}
            )
            return True
        except Exception as ex:
            print(f"❗core/news_scraper/logs_sender 錯誤: {ex}")
            return False
    logs_Sender_Printer(f"ℹ️news_scraper_starter任務啟動")
    logs_Sender_Printer(f"ℹ️爬取類別：{want_category}")
    logs_Sender_Printer(f"ℹ️每類數量：{each_num}")
    news_collector()
    return f"news_scraper_starter complete"

# 停用機制：一次爬取某個時間段內所有新聞
# from datetime import datetime, timedelta
# gole_Time = datetime.now() - timedelta(days=1)
# page_time = datetime.strptime(news_dict['date'], '%Y-%m-%d %H:%M')

# 停用：透過js內部請求新聞的api抓取新聞，用途為一次運行無限抓取新聞，直到條件滿足
# 停用原因：不穩定，沒必要
    # news_counter = 0
    # print("❗此處開始使用js內部請求新聞的api抓取新聞，可能不穩定❗")
    # print(f"停止條件：抓取新聞時間早於24小時前，或是抓取到第10頁")
    # print("gole_Time = ", gole_Time)
    # print("條件修改處：ANANews\\core\\news_scraper.py\n")
    # page_counter = 2
    # news_dict = {}
    # while True:
    #     if page_time < gole_Time:
    #         break
    #     if page_counter >= 10:
    #         break

    #     url = f"https://udn.com/api/more?page={page_counter}&id=&channelId=1&cate_id=0&type=breaknews"
    #     page_counter += 1

    #     page = requests.get(
    #         url, headers={'user-agent': user_agent.random}, timeout=5).json()
    #     time.sleep(1)
    #     for item in page["lists"]:

    #         news_link = item["titleLink"].replace(
    #             "?from=udn-ch1_breaknews-1-0-news", "")
    #         news_id = (int(news_link.split("/")
    #                    [3]), int(news_link.split("/")[4]))
    #         if news.db_is_news_exists(news_id):
    #             page_time = datetime.strptime(
    #                 news.db_get(news_id)["date"], '%Y-%m-%d %H:%M')
    #             print(f"🔸已收錄新聞：{news_id}")
    #         else:
    #             in_url = 'https://udn.com'+news_link
    #             in_req = requests.get(
    #                 in_url, headers={'user-agent': user_agent.random}, timeout=10)
    #             in_page = BeautifulSoup(in_req.text, 'lxml')

    #             news_dict = {
    #                 "date": item['time']["date"],
    #                 "category": in_page.find('nav', {"class": "article-content__breadcrumb"}).find_all("a")[1].get_text('', strip=True),
    #                 "title": item['title'],
    #                 "content": in_page.find('section', {"class": "article-content__editor"}).get_text('', strip=True),
    #                 "photo_link": item['url']}
    #             news.db_update(news_id, news_dict)
    #             print("新收錄新聞：", news_id)
    #             news_counter += 1
    #             page_time = datetime.strptime(
    #                 news_dict['date'], '%Y-%m-%d %H:%M')
    #             time.sleep(1)

    # print(f"本次一共新收錄{news_counter}份新聞")
