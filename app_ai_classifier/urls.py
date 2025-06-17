from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_sentiment, name='home_sentiment'),
    path('openai_talk', views.openai_talk, name='openai_talk'),

    path('api/get_sentiment/', views.get_sentiment, name='get_sentiment'),
    path('api/ai_connection/', views.ai_connection,
         name='ai_connection'),
    path('api/ai_talk/', views.ai_talk, name='ai_talk'),
    # path('api/person-data/', views.get_persons, name='get_persons'),
]
