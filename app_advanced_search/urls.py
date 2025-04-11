from django.urls import path
from app_advanced_search import views
urlpatterns = [
    path('', views.user_interest, name='user_interest'),
    path('user_interest/', views.user_interest, name='user_interest'),
    path('keyword_assoc/', views.keyword_assoc, name='keyword_assoc'),

    path('base/', views.base, name='base'),
    path("api/assoc_ana/", views.assoc_ana, name="assoc_ana"),
]
