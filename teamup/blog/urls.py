from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, remove_participant
from . import views
from .views import join_event, cancel_join_event, joined_events, joined_events_json, join_success_view, cancel_join_success_view, time_conflict_view


urlpatterns = [
    path('join-success/<int:post_id>/', join_success_view, name='join-success'),
    path('cancel-join-success/<int:post_id>/', cancel_join_success_view, name='cancel-join-success'),
    path('', views.homepage, name='teamup'),
    path('joined-events-json/', joined_events_json, name='joined-events-json'),
    path('remove_participant/<int:post_id>/<int:participant_id>/', remove_participant, name='remove-participant'),
    path('join_event/<int:post_id>/', views.join_event, name='join-event'),
    path('cancel_join_event/<int:post_id>/', cancel_join_event, name='cancel_join_event'),
    path('user/find_event', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('joined-events/', joined_events, name='joined-events'),
]