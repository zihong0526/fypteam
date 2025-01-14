from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta
from sport_list.models import Sport
from venue_list.models import Venue
from notifications.models import Notification

class Post(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancel','Cancel'),
    )

    # SPORT_CHOICES = (
    #     ('active', 'Active'),
    #     ('inactive', 'Inactive'),
    #     ('cancel', 'Cancel'),
    # )

    def get_sport_choices():
        return [(sport.name, sport.name) for sport in Sport.objects.all()]

    SPORT_CHOICES = get_sport_choices()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    sport_type = models.CharField(max_length=100, choices=SPORT_CHOICES, default='Basketball')
    location = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    participant_number = models.PositiveIntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    event_date = models.DateField(default=timezone.now())
    event_time = models.TimeField(default='12:00:00')
    event_end_time = models.TimeField(default='14:00:00')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    # Combine event_date and event_time into event_datetime
    @property
    def event_datetime(self):
        return datetime.combine(self.event_date, self.event_time)

    # Combine event_date and event_end_time into event_end_datetime
    @property
    def event_end_datetime(self):
        return datetime.combine(self.event_date, self.event_end_time).replace(tzinfo=timezone.utc)

    def check_and_update_status(self):
        current_datetime = timezone.now()

        if self.status == 'cancel':

            joined_users = self.participants.all()

            for joined_user in joined_users:
                Notification.objects.create(
                    user=joined_user,
                    message=f'The event "{self}" has been canceled. Your participation has been canceled.',
                    link=f'/posts/{self.id}/',
                )

            return


        if current_datetime > self.event_end_datetime:
            self.status = 'inactive'
            self.save()
        else:
            self.status = 'active'
            self.save()

    def joined_users_count(self):
        return self.participants.count()

    def __str__(self):
        return self.sport_type

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def venue_latitude(self):
        if self.location:
            return self.location.latitude
        return None

    def venue_longitude(self):
        if self.location:
            return self.location.longitude
        return None
