from django.urls import path
from .import views

urlpatterns = [
    path('chats/', views.get_chats, name='get_chats'),
    path('find_users/', views.get_find_users, name='find_users'),
    path('user_profile/', views.user_profile, name='user_profile')
]
