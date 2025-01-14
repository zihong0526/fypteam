from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
from .models import JoinRequest, Post

@login_required
def send_join_request(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has already joined or sent a request
    if request.user in post.participants.all():
        # User has already joined
        return HttpResponseRedirect(reverse('post-detail', args=[post.id]))

    # Check if there is a pending request
    if JoinRequest.objects.filter(user=request.user, event=post, status='pending').exists():
        # Pending request already exists
        return HttpResponseRedirect(reverse('post-detail', args=[post.id]))

    # Create a new join request
    JoinRequest.objects.create(user=request.user, event=post)
    return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
