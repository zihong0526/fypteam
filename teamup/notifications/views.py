from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Check if all notifications are unread
    all_unread = all(notif.is_unread for notif in notifications)
    return render(request, 'notifications/notification_list.html',
                  {'notifications': notifications, 'all_unread': all_unread})

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_unread = False
    notification.save()
    return redirect('notification-list')

def mark_all_as_read(request):
    Notification.objects.filter(user=request.user, is_unread=True).update(is_unread=False)
    return redirect('notification-list')