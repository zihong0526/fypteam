from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from friend.models import Friendss
from django.db import models
from .models import GroupChat, GroupMessage






@login_required
def unread_group_messages_count(request, group_chat_id):
    print("Group Chat ID:", group_chat_id)
    group_messages = GroupMessage.objects.filter(group_chat_id=group_chat_id)
    unread_count = sum(1 for group_message in group_messages if not group_message.is_read_by_user(request.user))
    print("Unread Count:", unread_count)
    return JsonResponse({'unread_group_messages_count': unread_count})


@login_required
def show_group_chats(request):
    group_chats = GroupChat.objects.filter(members=request.user)
    return render(request, 'message/show_group_chats.html', {'group_chats': group_chats})

@login_required
def group_chat(request, group_id):
    group_chat = get_object_or_404(GroupChat, id=group_id)
    members = group_chat.members.all()

    all_group_chats = GroupChat.objects.filter(members=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        GroupMessage.objects.create(sender=request.user, group_chat=group_chat, content=content)

    group_messages = group_chat.group_messages.order_by('timestamp')
    for group_message in group_messages:
        if not group_message.is_read_by_user(request.user):
            group_message.mark_as_read(request.user)

    return render(request, 'message/group_chat.html', {'group_chat': group_chat, 'members': members, 'group_messages': group_messages, 'all_group_chats': all_group_chats})


@login_required
def create_group(request):
    friends = Friendss.objects.get(user=request.user).friend.all()

    if request.method == 'POST':
        selected_friends = request.POST.getlist('selected_friends')
        group_name = request.POST.get('group_name')
        group_chat = GroupChat.objects.create(name=group_name)
        group_chat.members.add(request.user, *selected_friends)

        # Redirect to the created group chat
        return redirect('group-chat', group_id=group_chat.id)

    return render(request, 'message/create_group.html', {'friends': friends})

@login_required
def send_message(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    friends = Friendss.objects.get(user=request.user).friend.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)

    messages = Message.objects.filter(
        (models.Q(sender=request.user, recipient=recipient) | models.Q(sender=recipient, recipient=request.user))
    ).order_by('timestamp')


    return render(request, 'message/send_message.html', {'recipient': recipient, 'messages': messages})

@login_required
def message(request):
    friends = Friendss.objects.get(user=request.user).friend.all()

    return render(request, 'message/message.html', {'friends': friends})

@login_required
def unread_messages_count(request):
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_messages_count': unread_count})

@login_required
def mark_messages_as_read(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)

    # Update is_read status for the messages
    messages = Message.objects.filter(
        sender=recipient, recipient=request.user, is_read=False
    )
    messages.update(is_read=True)

    return redirect('send-message', recipient_username=recipient_username)