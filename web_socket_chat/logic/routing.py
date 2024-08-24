from django.urls import path
from . import consumers


ws_urlpatterns = [
    path('ws/chat/<int:pk>/', consumers.WSConsumer.as_asgi())
]
