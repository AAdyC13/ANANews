from django.urls import path
from app_special_ana import views
urlpatterns = [
    path('', views.president_Lai, name='president_Lai'),
    path('president_Lai/', views.president_Lai, name='president_Lai'),
    
    path('base/', views.base, name='base'),
    path("api/president_data/", views.president_data, name="president_data"),
]
