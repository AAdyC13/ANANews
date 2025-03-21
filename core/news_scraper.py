
def news_scraper():
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
    # import pandas as pd
    from .models import analysed_news as news
    from datetime import datetime, timedelta
    import time

    user_agent = UserAgent()
    gole_Time = datetime.now() - timedelta(days=1)
    # 在【聯合新聞網】的【即時】主頁，底下有【不分類】即時列表，我打算批量抓這裡的新聞
    url = 'https://udn.com/news/breaknews/1/99#breaknews'
    req = requests.get(
        url, headers={'user-agent': user_agent.random}, timeout=5)
    page = BeautifulSoup(req.text, 'lxml')
    news_dict = {}
    news_counter = 0

    for single_news in page.find_all('a', {"class": "story-list__image--holder", 'data-content_level': "開放閱讀"}):
        if single_news.get('href'):
            news_link = single_news.get('href').replace(
                "?from=udn-ch1_breaknews-1-99-news", "")
            news_id = (news_link.split("/")[3], news_link.split("/")[4])

            if news.db_is_news_exists(news_id):
                page_time = datetime.strptime(
                    news.db_get(news_id)["date"], '%Y-%m-%d %H:%M')
                print(f"🔸已收錄新聞：{news_id}")
            else:

                in_url = 'https://udn.com'+news_link
                in_req = requests.get(
                    in_url, headers={'user-agent': user_agent.random}, timeout=50)
                in_page = BeautifulSoup(in_req.text, 'lxml')
                # 重要：replace("&", "&amp;")是必要的，網站伺服器會針對 & 和 &amp 傳輸兩張不一樣的圖片，
                # 據觀察，好像是大圖和縮小圖，縮小圖應該是為了不占用資源的版本
                news_picture = single_news.find(
                    'source', {"type": "image/webp"})

                news_dict = {"date": in_page.find('div', {"class": "article-content__subinfo"}).find('section', {"class": "authors"}).find('time', {"class": "article-content__time"}).get_text('', strip=True),
                             "category": in_page.find('nav', {"class": "article-content__breadcrumb"}).find_all("a")[1].get_text('', strip=True),
                             "title": single_news.get('aria-label'),

                             # 重要：這裡的內文無誤，但沒有分段，所以若之後要讓這個文本自帶分段，可以回來調整
                             "content": in_page.find('section', {"class": "article-content__editor"}).get_text('', strip=True),

                             "photo_link": news_picture.get('srcset').replace("&", "&amp;")}
                news.db_update(news_id, news_dict)
                print("新收錄新聞：", news_id)
                page_time = datetime.strptime(
                    news_dict['date'], '%Y-%m-%d %H:%M')
                news_counter += 1
                time.sleep(1)
    print(f"本次一共新收錄{news_counter}份新聞\n")

    news_counter = 0
    print("❗此處開始使用js內部請求新聞的api抓取新聞，可能不穩定❗")
    print(f"停止條件：抓取新聞時間早於24小時前，或是抓取到第10頁")
    print("gole_Time = ", gole_Time)
    print("條件修改處：ANANews\\core\\news_scraper.py\n")
    page_counter = 2
    news_dict = {}
    while True:
        if page_time < gole_Time:
            break
        if page_counter >= 10:
            break

        url = f"https://udn.com/api/more?page={page_counter}&id=&channelId=1&cate_id=0&type=breaknews"
        page_counter += 1

        page = requests.get(
            url, headers={'user-agent': user_agent.random}, timeout=5).json()
        time.sleep(1)
        for item in page["lists"]:

            news_link = item["titleLink"].replace(
                "?from=udn-ch1_breaknews-1-0-news", "")
            news_id = (int(news_link.split("/")
                       [3]), int(news_link.split("/")[4]))
            if news.db_is_news_exists(news_id):
                page_time = datetime.strptime(
                    news.db_get(news_id)["date"], '%Y-%m-%d %H:%M')
                print(f"🔸已收錄新聞：{news_id}")
            else:
                in_url = 'https://udn.com'+news_link
                in_req = requests.get(
                    in_url, headers={'user-agent': user_agent.random}, timeout=10)
                in_page = BeautifulSoup(in_req.text, 'lxml')

                news_dict = {
                    "date": item['time']["date"],
                    "category": in_page.find('nav', {"class": "article-content__breadcrumb"}).find_all("a")[1].get_text('', strip=True),
                    "title": item['title'],
                    "content": in_page.find('section', {"class": "article-content__editor"}).get_text('', strip=True),
                    "photo_link": item['url']}
                news.db_update(news_id, news_dict)
                print("新收錄新聞：", news_id)
                news_counter += 1
                page_time = datetime.strptime(
                    news_dict['date'], '%Y-%m-%d %H:%M')
                time.sleep(1)

    print(f"本次一共新收錄{news_counter}份新聞")
