import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ANANews.routing  # 確保這裡導入 routing.py

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ANANews.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # 使用 AuthMiddleware 來支援 Django 使用者身份
        URLRouter(
            ANANews.routing.websocket_urlpatterns  # 確保這裡正確對應
        )
    ),
})
print("ANANews\\ANANews\\asgi.py被讀取")
