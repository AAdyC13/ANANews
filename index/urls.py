from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path('web_intro', views.web_intro, name='me.html'),
    path("api/get_news_DBinfo/", views.get_news_DBinfo, name="get_news_DBinfo"),
    path("api/news_scraper_start/", views.news_scraper_start, name="news_scraper_start"),
    path("api/check_scraper_isWork/", views.check_scraper_isWork, name="check_scraper_isWork"),
    
]
