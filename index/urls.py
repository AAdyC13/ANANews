from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path("api/get_news_DBinfo/", views.get_news_DBinfo, name="get_news_DBinfo"),
    path("api/news_scraper_start/", views.news_scraper_start, name="news_scraper_start"),
    
]
