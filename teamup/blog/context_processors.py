from notifications.models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_unread=True)
        return {'unread_notifications': unread_notifications}
    return {'unread_notifications': []}