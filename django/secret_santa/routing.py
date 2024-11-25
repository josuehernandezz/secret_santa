# routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # Capture group_code from the URL
    path('ws/ticks/<str:group_code>', consumers.TicksSyncConsumer.as_asgi()),
]
