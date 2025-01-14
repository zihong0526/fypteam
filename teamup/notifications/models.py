from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Notification(models.Model):
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    is_unread = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('notification-detail', args=[str(self.id)])
