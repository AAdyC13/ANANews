from django.urls import path
from app_llm_report import views
urlpatterns = [
    path('', views.llm_report, name='llm_report'),
    path('ollama/', views.llm_report, name='llm_report'),
    # path('top_keyword/', views.top_keyword, name='top_keyword'),
    # path('top_person/', views.top_person, name='top_person'),

    path('base/', views.base, name='base'),
    path("api/ollama_request/", views.ollama_request, name="ollama_request"),
    # path('api/get-categories/', views.get_categories, name='get_categories'),
    # path('api/person-data/', views.get_persons, name='get_persons'),
]
