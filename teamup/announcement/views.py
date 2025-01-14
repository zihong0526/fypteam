from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcementss, Comment, AnnouncementPermission
from django.contrib.auth.decorators import login_required
from .forms import AnnouncementForm
from notifications.models import Notification
from django.contrib.auth.models import User

@login_required
def create_announcement(request):

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()

            users = User.objects.exclude(pk=announcement.author.id)
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f'New announcement: {announcement.title}',
                    link=f'/path-to-announcement/{announcement.id}/'
                )

            return redirect('announcement')

    else:
        form = AnnouncementForm()
    return render(request, 'announcement/create_announcement.html', {'form': form})


@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcementss, pk=announcement_id)

    if request.user != announcement.author:
        return redirect('announcement')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'announcement/edit_announcement.html', {'form': form, 'announcement': announcement})

@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcementss, pk=announcement_id)

    if request.user != announcement.author:
        return redirect('announcement')

    if request.method == 'POST':
        return redirect('delete_announcement', announcement.id)


    return render(request, 'announcement/delete_announcement.html', {'announcement': announcement})


@login_required
def confirm_delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcementss, pk=announcement_id)

    if request.user != announcement.author:
        return redirect('announcement')

    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement')

    return render(request, 'announcement/delete_announcement.html', {'announcement': announcement})


@login_required
def announcement(request):
    announcement_permissions_list = AnnouncementPermission.objects.filter(users_with_permissions=request.user)
    context = {
        'announcements': Announcementss.objects.all(),
        'announcement_permissions_list': announcement_permissions_list,
    }
    return render(request, 'announcement/announcement.html', context)

@login_required
def add_comment_to_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcementss, pk=announcement_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(announcement=announcement, author=request.user, text=text)
    return redirect('announcement')

@login_required
def like_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcementss, pk=announcement_id)
    if request.user in announcement.likes.all():
        announcement.likes.remove(request.user)
    else:
        announcement.likes.add(request.user)
    return redirect('announcement')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the user is the author of the comment
    if request.user == comment.author:
        comment.delete()

    return redirect('announcement')