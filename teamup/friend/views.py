from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Friend, Friendss
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from notifications.models import Notification


@login_required
def sent_list(request):
    # Get the current user's friends
    friends = Friend.objects.filter(user=request.user)

    return render(request, 'friend/sent_request.html', {'friends': friends})

@login_required
def friend_list(request):
    # Get the current user's friends
    friends = Friendss.objects.filter(user=request.user)

    return render(request, 'friend/friend_list.html', {'friends': friends})

@login_required
def friend_request_list(request, username):
    user = User.objects.get(username=username)
    followers = Friend.objects.filter(friend=user)
    return render(request, 'friend/friend_request.html', {'user': user, 'followers': followers})

@login_required
def handle_friend_request(request):
    if request.method == 'POST':
        follower_id = request.POST.get('follower_id')
        action = request.POST.get('action')

        try:
            follower = Friend.objects.get(id=follower_id, friend=request.user)
        except Friend.DoesNotExist:
            return JsonResponse({'error': 'Invalid request'})

        if action == 'accept':
            # Use a transaction to ensure consistency
            with transaction.atomic():
                # Add the follower to Friendss model for the current user
                friendss_instance, created = Friendss.objects.get_or_create(user=request.user)
                friendss_instance.friend.add(follower.user)

                # Add the current user to Friendss model for the follower
                follower_friendss_instance, _ = Friendss.objects.get_or_create(user=follower.user)
                follower_friendss_instance.friend.add(request.user)

                Notification.objects.create(
                    user=follower.user,
                    message=f'{request.user.username} accepted your friend request.',
                    link=f'/user/{request.user.username}/',
                )

                # Delete the friend request from Friend model
                follower.delete()
        elif action == 'reject':
            # Delete the friend request from Friend model
            follower.delete()

        return redirect('friend-request', username=request.user.username)

    return JsonResponse({'error': 'Invalid request'})

@login_required
def delete_friend_request(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')

        try:
            friend_request = Friend.objects.get(id=friend_id, user=request.user)
            friend_request.delete()
        except Friend.DoesNotExist:
            pass  # Handle the case where the friend request doesn't exist

    return redirect('sent-request')

@login_required
def delete_friend(request):
    if request.method == 'GET':
        friend_id = request.GET.get('friend_id')
        friend_user = get_object_or_404(User, id=friend_id)
        return render(request, 'friend/confirm_delete_friend.html', {'friend_user': friend_user})

    elif request.method == 'POST':
        friend_id = request.POST.get('friend_id')

        try:
            # Get the friend's user object
            friend_user = User.objects.get(id=friend_id)

            # Remove the friend from the current user's Friendss model
            current_user_friendss = Friendss.objects.get(user=request.user)
            current_user_friendss.friend.remove(friend_user)

            # Remove the current user from the friend's Friendss model
            friend_friendss = Friendss.objects.get(user=friend_user)
            friend_friendss.friend.remove(request.user)

        except User.DoesNotExist:
            pass  # Handle the case where the user doesn't exist

        return redirect('friend')

    return JsonResponse({'error': 'Invalid request'})