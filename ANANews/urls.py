from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('app_top_keyword.urls'))
]
