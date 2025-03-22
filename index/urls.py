from django.urls import path
from index import views
#from .views import get_chart_data,get_categories

urlpatterns = [
    path('', views.index, name='index.html'),
    # path("api/chart-data/", get_chart_data, name="chart-data"),
    # path('get-categories/', get_categories, name='get_categories'),
]
