from django.urls import re_path
from .consumers import CeleryLogConsumer  # 確保這裡導入正確的 Consumer

websocket_urlpatterns = [
    re_path(r"ws/celery-logs/$", CeleryLogConsumer.as_asgi()),  # 確保這裡的路由與前端相符
]