from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('index/', include('index.urls')),

    path('top/', include('app_top_keyword.urls')),
    path('special_ana/', include('app_special_ana.urls')),
    path('advanced_search/', include('app_advanced_search.urls')),
    path('llm_report/', include('app_llm_report.urls')),

    # 最初是和llm_report做在一起，分開要處裡太多，懶得改，只改版面
    path('ai_sentiment/', include('app_llm_report.urls')),
]
