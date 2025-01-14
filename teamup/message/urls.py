from django.urls import path
from .views import send_message, message, unread_messages_count, mark_messages_as_read, create_group, group_chat, show_group_chats, unread_group_messages_count

urlpatterns = [
    path('group/<int:group_id>/', group_chat, name='group-chat'),
    path('create-group/', create_group, name='create-group'),
    path('show-group-chats/', show_group_chats, name='show-group-chats'),
    path('send-message/<str:recipient_username>/', send_message, name='send-message'),
    path('message/', message, name='message'),
    path('unread-messages-count/', unread_messages_count, name='unread-messages-count'),
    path('message/mark-messages-as-read/<str:recipient_username>/', mark_messages_as_read, name='mark-messages-as-read'),
    path('message/unread-group-messages-count/<int:group_chat_id>/', unread_group_messages_count, name='unread-group-messages-count'),


]
