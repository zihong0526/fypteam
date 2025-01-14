from django import template
from join_requests.models import JoinRequest

register = template.Library()

@register.filter(name='user_join_status')
def user_join_status(user, event):
    # Check if the user has a pending join request for the event
    pending_request_exists = JoinRequest.objects.filter(user=user, event=event, status='pending').exists()

    # Check if the user has joined the event
    has_joined_event = user in event.participants.all()

    if has_joined_event:
        return 'joined'
    elif pending_request_exists:
        return 'pending'
    else:
        return 'not_joined'

@register.filter
def has_pending_request(user, event):
    return JoinRequest.objects.filter(user=user, event=event, status='pending').exists()

@register.filter
def has_joined_event(user, event):
    return user in event.participants.all()
