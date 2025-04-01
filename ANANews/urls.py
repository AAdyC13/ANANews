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
]
