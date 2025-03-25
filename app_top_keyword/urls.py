from django.urls import path
from app_top_keyword import views
urlpatterns = [
    path('', views.top_keyword, name='top_keyword'),
    path('top_keyword/', views.top_keyword, name='top_keyword'),
    path('top_person/', views.top_person, name='top_person'),
    path('user_interest/', views.user_interest, name='user_interest'),
    
    path('base/', views.base, name='base'),
    path("api/chart-data/", views.get_chart_data, name="chart-data"),
    path('api/get-categories/', views.get_categories, name='get_categories'),
    path('api/person-data/', views.get_persons, name='get_persons'),
    path('api/interest-data/', views.get_user_interest, name='get_user_interest'),
]
