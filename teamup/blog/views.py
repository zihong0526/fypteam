from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Sport
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date, datetime
from django.contrib import messages
from notifications.models import Notification
from .models import Venue

@login_required
def cancel_join_success_view(request, post_id):
    message = request.GET.get('message', '')
    # You can also retrieve the post information using post_id if needed
    return render(request, 'blog/cancel_join_success.html', {'post_id': post_id, 'message': message})

@login_required
def join_success_view(request, post_id):
    message = request.GET.get('message', '')
    # You can also retrieve the post information using post_id if needed
    return render(request, 'blog/join_success.html', {'post_id': post_id, 'message': message})

@login_required
def time_conflict_view(request):
    return render(request, 'blog/time_conflict_message.html')

@login_required
def remove_participant(request, post_id, participant_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user making the request is the author of the post
    if request.user == post.author:
        participant = get_object_or_404(post.participants, id=participant_id)
        post.participants.remove(participant)

        # Update the event status if needed
        post.check_and_update_status()

        Notification.objects.create(
            user=participant,
            message=f'You have been removed from the event "{post}"',
            link=f'/posts/{post_id}/',
        )
        messages.success(request, f'Participant {participant.username} removed successfully.')
        return JsonResponse({'status': 'success'})
    else:
        messages.error(request, 'Permission denied.')
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})

@login_required
def cancel_join_event(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.participants.all():
        post.participants.remove(user)
        post.check_and_update_status()
        post.save()

    Notification.objects.create(
        user=user,
        message=f'You have canceled your participation in the event "{post}"',
        link=f'/posts/{post_id}/',
    )
    # Notify the event creator
    if user != post.author:
        Notification.objects.create(
            user=post.author,
            message=f'User "{user}" has canceled their participation in your event "{post}"',
            link=f'/posts/{post_id}/',
        )

    return JsonResponse({'participant_count': post.joined_users_count()})

@login_required
def join_event(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.participants.all():
        # User already joined, remove from participants
        post.participants.remove(user)
        status = 'canceled'

        Notification.objects.create(
            user=user,
            message=f'You have been removed from the event "{post}"',
            link=f'/posts/{post_id}/',
        )

        messages.success(request, 'Successfully canceled your participation in the event.')

    else:
        # Check for time conflicts before joining
        conflicting_event = has_time_conflict(user, post)

        if conflicting_event:
            message = 'Time conflict! You cannot join the event "{post}" because of a conflict with another event.'
            alert_message = f'<p class="text-danger">{message}</p>'
            return render(request, 'blog/time_conflict_message.html', {'alert_message': alert_message})

        # User is joining, add to participants
        post.participants.add(user)
        status = 'joined'

        Notification.objects.create(
            user=user,
            message=f'You are successfully joined the event "{post}"',
            link=f'/posts/{post_id}/',
        )

        # Notify the event creator
        if user != post.author:
            Notification.objects.create(
                user=post.author,
                message=f'User "{user}" has joined your event "{post}"',
                link=f'/posts/{post_id}/',
            )

        messages.success(request, 'Successfully joined the event.')

        messages.success(request, 'Successfully joined the event.')

    participant_count = post.participants.count()
    post.check_and_update_status()

    return JsonResponse({'status': status, 'participant_count': participant_count})

def has_time_conflict(user, new_event):
    # Fetch all events that the user is participating in
    user_events = Post.objects.filter(participants=user)

    # Check for time conflicts with the new event
    for event in user_events:
        if event.event_date == new_event.event_date:
            if event.event_end_time > new_event.event_time and event.event_time < new_event.event_end_time:
                return event

    return False

def homepage(request):
    update_all_posts_status()
    return render(request, 'blog/teamup.html')

def update_all_posts_status():
    all_posts = Post.objects.all()
    for post in all_posts:
        post.check_and_update_status()
        post.save()

@login_required
def home(request):
    today = date.today()
    current_time = datetime.now().time()
    update_all_posts_status()
    sports = Sport.objects.all()
    venues = Venue.objects.all()

    context = {
        'today': today,
        'current_time': current_time,
        'posts': Post.objects.order_by('-date_posted'),
        'sports': sports,
        'venues': venues,
    }
    return render(request, 'blog/home.html', context)



class PostListView(ListView):

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    venues = Venue.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_all_posts_status()

        # Fetch the sports list from the Sport model
        context['sports'] = Sport.objects.all()
        context['venues'] = Venue.objects.all()

        sport_type = self.request.GET.get('sport_type', '')
        location = self.request.GET.get('location', '')
        event_date = self.request.GET.get('event_date', '')
        queryset = Post.objects.order_by('-date_posted')

        if sport_type:
            queryset = queryset.filter(sport_type__icontains=sport_type)

        if location:
            queryset = queryset.filter(location__name__icontains=location)

        if event_date:
            # Assuming the date format is 'YYYY-MM-DD'
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
                queryset = queryset.filter(event_date=event_date)
            except ValueError:
                # Handle invalid date format if needed
                pass

        context['posts'] = queryset
        return context



class UserPostListView(ListView):
        model = Post
        template_name = 'blog/user_posts.html'
        context_object_name = 'posts'
        paginate_by = 10

        def get_queryset(self):
            user = get_object_or_404(User, username=self.kwargs.get('username'))
            return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['sport_type', 'location', 'participant_number', 'event_time', 'event_date', 'event_end_time', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Create a notification for the user who created the post
        Notification.objects.create(
            user=self.request.user,
            message=f'Your post "{self.object}" has been created successfully.',
            link=f'/path-to-post/{self.object.id}/'  # Adjust the link as needed
        )

        # Add a success message for the user
        messages.success(self.request, 'Post created successfully!')

        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['sport_type','location','participant_number','event_time','event_date','event_end_time','status']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def joined_events(request):
    user = request.user
    joined_events = Post.objects.filter(participants=user).order_by('-date_posted')

    context = {
        'joined_events': joined_events,
        'receiver_profile': None,
    }

    return render(request, 'blog/joined_events.html', context)

@login_required
def joined_events_json(request):
    user = request.user
    joined_events = Post.objects.filter(participants=user)

    # Convert joined events to a JSON-serializable format
    joined_events_json = [
        {
            'sport_type': event.sport_type,
            'event_datetime': event.event_datetime.isoformat(),
            'event_end_datetime': event.event_end_datetime.isoformat(),
        }
        for event in joined_events
    ]

    return JsonResponse({'joined_events': joined_events_json})