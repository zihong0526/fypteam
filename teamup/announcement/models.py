from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AnnouncementPermission(models.Model):
    users_with_permissions = models.ManyToManyField(User, related_name='announcement_permissions', blank=True)

class Announcementss(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default='12:00:00')
    likes = models.ManyToManyField(User, related_name='announcement_likes', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='announcement_comments', blank=True)


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    announcement = models.ForeignKey(Announcementss, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text