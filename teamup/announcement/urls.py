from django.urls import path
from .views import announcement, add_comment_to_announcement, like_announcement,delete_comment, create_announcement, edit_announcement, delete_announcement, confirm_delete_announcement
from . import views

urlpatterns = [
        path('announcement/', announcement, name='announcement'),
        path('announcement/<int:announcement_id>/comment/', add_comment_to_announcement,
             name='add_comment_to_announcement'),
        path('announcement/<int:announcement_id>/like/', like_announcement, name='like_announcement'),
        path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
        path('create_announcement/', create_announcement, name='create_announcement'),
        path('edit_announcement/<int:announcement_id>/', edit_announcement, name='edit_announcement'),
        path('delete_announcement/<int:announcement_id>/', delete_announcement, name='delete_announcement'),
        path('confirm_delete_announcement/<int:announcement_id>/', confirm_delete_announcement, name='confirm_delete_announcement'),


]