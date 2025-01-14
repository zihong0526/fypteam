from django.db import models
from users.models import Profile

class Feedback(models.Model):
    giver = models.ForeignKey(Profile, related_name='given_feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='received_feedback', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Calculate average rating for the receiver
        feedbacks = Feedback.objects.filter(receiver=self.receiver)
        total_ratings = feedbacks.count()
        average_rating = feedbacks.aggregate(models.Avg('rating'))['rating__avg']
        average_rating = 5.0 if average_rating is None else average_rating
        # Update receiver's profile
        self.receiver.total_ratings = total_ratings
        self.receiver.average_rating = average_rating
        self.receiver.save()