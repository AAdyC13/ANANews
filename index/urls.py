from django.urls import path
from index import views

from .views import get_news_DBinfo

urlpatterns = [
    path('', views.index, name='index.html'),
    path("api/get_news_DBinfo/", get_news_DBinfo, name="get_news_DBinfo"),
    
]
