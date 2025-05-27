from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_sentiment, name='home_sentiment'),

    path('api/get_sentiment/', views.get_sentiment, name='get_sentiment'),
    # path('api/person-data/', views.get_persons, name='get_persons'),
]
