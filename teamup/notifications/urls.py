from django.urls import path
from .views import notification_list, mark_as_read, mark_all_as_read

urlpatterns = [
    path('', notification_list, name='notification-list'),
    path('notifications/mark-as-read/<int:notification_id>/', mark_as_read, name='mark-as-read'),
    path('notifications/mark-all-as-read/', mark_all_as_read, name='mark-all-as-read'),
   ]
