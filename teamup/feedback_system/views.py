from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Feedback
from .forms import FeedbackForm
from users.models import Profile

def leave_feedback(request, receiver_profile_id):
    receiver_profile = get_object_or_404(Profile, id=receiver_profile_id)

    # Check if the user has already left feedback for the receiver
    feedback_already_given = Feedback.objects.filter(giver=request.user.profile, receiver=receiver_profile).exists()

    # Check if the user is trying to leave feedback for themselves
    feedback_for_self = request.user.profile == receiver_profile

    if feedback_for_self:
        # If the user is trying to leave feedback for themselves, you can redirect them or display a message
        return render(request, 'feedback_system/feedback_for_self.html', {'receiver_profile': receiver_profile, 'feedback_for_self': feedback_for_self})

    if feedback_already_given:
        # If feedback has already been given, you can redirect the user or display a message
        return render(request, 'feedback_system/already_given_feedback.html', {'receiver_profile': receiver_profile, 'feedback_for_self': feedback_for_self})

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.giver = request.user.profile
            feedback.receiver = receiver_profile
            feedback.save()

            # Update average rating for the receiver
            average_rating = Feedback.objects.filter(receiver=receiver_profile).aggregate(Avg('rating'))['rating__avg']
            receiver_profile.average_rating = average_rating
            receiver_profile.save()

            return redirect('joined-events')
    else:
        form = FeedbackForm()

    return render(request, 'feedback_system/feedback_form.html', {'form': form, 'receiver_profile': receiver_profile, 'feedback_for_self': feedback_for_self})

def view_feedback(request, receiver_profile_id):
    receiver_profile = get_object_or_404(Profile, id=receiver_profile_id)


    participants_feedback = Feedback.objects.filter(receiver=receiver_profile).exclude(giver=receiver_profile)

    return render(request, 'feedback_system/view_feedback.html', {'receiver_profile': receiver_profile, 'participants_feedback': participants_feedback})