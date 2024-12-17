import os
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Notifications.routing import websocket_urlpatterns

logger = logging.getLogger("django")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmate.settings')

logger.debug("ASGI application started")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
