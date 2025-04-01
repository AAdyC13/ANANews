from django.urls import path
from app_special_ana import views
urlpatterns = [
    path('', views.president_Lai, name='president_Lai'),
    path('president_Lai/', views.president_Lai, name='president_Lai'),
    
    path('base/', views.base, name='base'),
    #path("api/chart-data/", views.get_chart_data, name="chart-data"),
]
