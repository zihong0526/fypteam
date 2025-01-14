from django.urls import path
from .views import friend_list, friend_request_list, sent_list, handle_friend_request, delete_friend_request, delete_friend

urlpatterns = [
    path('friend/', friend_list, name='friend'),
    path('sent-request/', sent_list, name='sent-request'),
    path('friend-request/<str:username>/', friend_request_list, name='friend-request'),
    path('handle-friend-request/', handle_friend_request, name='handle-friend-request'),
    path('delete-friend-request/', delete_friend_request, name='delete-friend-request'),
    path('delete-friend/', delete_friend, name='delete-friend'),
]