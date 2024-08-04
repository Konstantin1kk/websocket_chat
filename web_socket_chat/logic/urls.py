from django.urls import path
from .import views

urlpatterns = [
    path('chats/', views.get_chats, name='get_chats'),
    path('chat/<int:pk>', views.ChatView.as_view(), name='get_chat'),
    path('create_chat/<int:pk>', views.CreateChatView.as_view(), name='create_chat'), # <-- redirect to
    path('find_users/', views.FindUsersListView.as_view(), name='find_users'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.Login.as_view(), name='registration'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
