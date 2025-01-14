from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    # You can add other fields as needed, such as date_added, etc.

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

class Meta:
    app_label = 'friend'


class Friendss(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ManyToManyField(User, related_name='freind', blank=True)
    # You can add other fields as needed, such as date_added, etc.

    def __str__(self):
        return f"{self.user} - {self.friend}"