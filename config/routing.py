from config.consumers import NotificationConsumer
from django.urls import path


websocket_urlpatterns = [
    path('notification/', NotificationConsumer.as_asgi(), name='notification')
]
