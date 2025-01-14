from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from friend.models import Friend, Friendss
from sport_list.models import Sport
from notifications.models import Notification
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Sqrt
from django.db import connection

def password_change_success(request):
    return render(request, 'users/password_change_success.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password-change-success')  # Redirect to a new success template
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to login')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form':form})

@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your info has been updated')
            return redirect('profile')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)



    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def user_profile_list(request):
    current_user = request.user
    profiles = Profile.objects.exclude(user=current_user)
    sports_list = Sport.objects.all()
    friend_list = Friendss.objects.get(user=current_user).friend.all()

    # Get filter parameters from the request
    sport_filter = request.GET.getlist('sport')
    skill_level_filter = request.GET.get('skill_level')
    location_filter = request.GET.get('location')
    gender_filter = request.GET.get('gender')

    # Check if at least one filter (other than sport) is selected
    other_filters_selected = any([skill_level_filter, location_filter, gender_filter])

    # Apply filters to the profiles queryset
    if sport_filter and any(sport_filter_item.strip() for sport_filter_item in sport_filter):
        profiles = profiles.filter(
            Q(sport_1__in=sport_filter) |
            Q(sport_2__in=sport_filter) |
            Q(sport_3__in=sport_filter)
        )

    # Apply other filters
    if location_filter:
        profiles = profiles.filter(location__icontains=location_filter)

    if gender_filter:
        profiles = profiles.filter(gender=gender_filter)

    if skill_level_filter:
        profiles = profiles.filter(
            Q(skill_level_1=skill_level_filter) |
            Q(skill_level_2=skill_level_filter) |
            Q(skill_level_3=skill_level_filter)
        )

    #detect added
    for profile in profiles:
        profile.is_friend = profile.user in friend_list

    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        friend_user = User.objects.get(username=friend_username)

        # Check if the friend_user is not already a friend
        if friend_user not in friend_list:
            Notification.objects.create(
                user=friend_user,
                message=f'{current_user.username} sent you a friend request.',
                link=f'/friend-request/{current_user.username}/',
            )

            # Add the friend_user to the Friend model
            Friend.objects.create(user=current_user, friend=friend_user)
            # Update the friend_list
            friend_list = Friendss.objects.get(user=current_user).friend.all()
            for profile in profiles:
                profile.is_friend = profile.user in friend_list


    context = {
        'profiles': profiles,
        'sports_list': sports_list,
        'sport_filter': sport_filter,
        'skill_level_filter': skill_level_filter,
        'location_filter': location_filter,
        'gender_filter': gender_filter,

    }

    # Calculate distance and order profiles by distance
    profiles = profiles.annotate(
        distance=ExpressionWrapper(
            Sqrt(
                (F('latitude') - current_user.profile.latitude) ** 2 +
                (F('longitude') - current_user.profile.longitude) ** 2
            ) * 100,
            output_field=FloatField()

        )
    ).order_by('distance')

    for profile in profiles:
        print(f"Latitude: {profile.latitude}, Longitude: {profile.longitude}, Distance: {profile.distance}")

    print(f"Current User Latitude: {current_user.profile.latitude}, Longitude: {current_user.profile.longitude}")
    print(connection.queries)

    return render(request, 'users/user_profile_list.html', context)



