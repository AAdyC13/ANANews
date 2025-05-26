from django.urls import path
from app_llm_report import views
urlpatterns = [
    path('', views.llm_report, name='llm_report'),
    path('ollama/', views.llm_report, name='llm_report'),
    path('my_bert/', views.my_bert, name='my_bert'),

    path('base/', views.base, name='base'),
    path("api/ollama_request/", views.ollama_request, name="ollama_request"),
    path("api/my_bert_ana/", views.my_bert_ana, name="my_bert_ana"),
    # path('api/get-categories/', views.get_categories, name='get_categories'),
    # path('api/person-data/', views.get_persons, name='get_persons'),
]
