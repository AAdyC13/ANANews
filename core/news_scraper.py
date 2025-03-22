from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from .models import analysed_news as news
import time

# 停用機制：一次爬取某個時間段內所有新聞
# from datetime import datetime, timedelta
# gole_Time = datetime.now() - timedelta(days=1)
# page_time = datetime.strptime(news_dict['date'], '%Y-%m-%d %H:%M')

user_agent = UserAgent()
def web_requester(url: str) -> BeautifulSoup|None:
    """網頁爬蟲
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
        print(f"❗core/news_scraper/web_requester 爬取失敗: {e}")
        return None

def news_story_extract(news_link: str) -> dict:
    in_page = web_requester('https://udn.com'+news_link)
    if in_page:
        # 重要：replace("&", "&amp;")是必要的，網站伺服器會針對 & 和 &amp 傳輸兩張不一樣的圖片，據觀察，好像是大圖和縮小圖，縮小圖應該是為了不占用資源的版本
        try:
            return{
                "date": in_page.find('div', {"class": "article-content__subinfo"}).find('section', {"class": "authors"}).find('time', {"class": "article-content__time"}).get_text('', strip=True),
                "category": in_page.find('nav', {"class": "article-content__breadcrumb"}).find_all("a")[1].get_text('', strip=True),
                "content": in_page.find('section', {"class": "article-content__editor"}).get_text('', strip=True),
            }
        except AttributeError as e:
            print(f"❗core/news_scraper/news_story_extract 找不到對應資料，回傳空字典: {e}")
            return {}
        except IndexError as e:
            print(f"❗core/news_scraper/news_story_extract 內文category的find_all()[1]出錯，回傳空字典: {e}")
            return {}

def news_collector_one() -> bool:
    """
    從【聯合新聞網】的【即時】頁面底下\n
    抓取頁面回傳的【娛樂】【科技】類新聞(數量因各種情況受影響)
    並存入資料庫
    Returns:
        bool: 是否成功
    """
    print("開始爬取【娛樂】【科技】類新聞")
    pages = [web_requester('https://udn.com/news/breaknews/1/8#breaknews'),web_requester('https://udn.com/news/breaknews/1/13#breaknews')]
    for page in pages:
        if(page):
            news_counter = 0
            for each_news in page.find_all('a', {"class": "story-list__image--holder", 'data-content_level': "開放閱讀"}):
                news_dict = {}
                if each_news.get('href'):
                    news_link = each_news.get('href').replace(
                        "?from=udn-ch1_breaknews-1-99-news", "")
                    news_id = (news_link.split("/")[3], news_link.split("/")[4])

                    if news.db_is_news_exists(news_id):
                        print(f"🔸已收錄新聞：{news_id}")
                    else:
                        news_dict = {
                            "title": each_news.get('aria-label'),
                            "photo_link": each_news.find('source', {"type": "image/webp"}).get('srcset').replace("&", "&amp;")
                        }| news_story_extract(news_link)
                        if news.db_update(news_id, news_dict):
                            print("新收錄新聞：", news_id)
                            news_counter += 1
                        else:
                            print("❗收錄新聞失敗：", news_id)
            print(f"本次一共新收錄{news_counter}份新聞\n")

def news_collector_two() -> bool:
    """
    從【聯合新聞網】的⬇️專欄底下\n
    【要聞】,【運動】,【全球】,【社會】,【地方】,【兩岸】,【Oops】,\n
    【產經】,【股市】,【生活】,【文教】,【評論】,【旅遊】\n
    抓取頁面回傳的新聞(數量因各種情況受影響)
    並存入資料庫
    Returns:
        bool: 是否成功
    """
    
    
    
    
    
    
    
    
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
