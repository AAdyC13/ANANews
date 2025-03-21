from django.urls import path
from app_top_keyword import views
from .views import get_chart_data,get_categories

urlpatterns = [
    path('', views.home, name='home'),
    path("api/chart-data/", get_chart_data, name="chart-data"),
    path('get-categories/', get_categories, name='get_categories'),
]
