from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/power_readings/$", consumers.PowerReadingsConsumer.as_asgi()),
]
