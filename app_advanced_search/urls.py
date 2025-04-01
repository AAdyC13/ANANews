from django.urls import path
from app_advanced_search import views
urlpatterns = [
    path('', views.user_interest, name='user_interest'),
    path('user_interest/', views.user_interest, name='user_interest'),
    
    path('base/', views.base, name='base'),
    #path("api/chart-data/", views.get_chart_data, name="chart-data"),
]
