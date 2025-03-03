# routing.py

from django.urls import path
from django.urls import re_path
from .consumers import ChatConsumer

urlpatterns = [
    re_path(r'ws/chat/(?P<sender>\w+)/(?P<recipient>\w+)/$', ChatConsumer.as_asgi()),
]
