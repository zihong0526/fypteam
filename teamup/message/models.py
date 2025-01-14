from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username} - {self.timestamp}"

class GroupChat(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=255, default='Group Chat')

    def __str__(self):
        return self.name

class GroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='group_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    readers = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def mark_as_read(self, user):
        self.readers.add(user)
        self.save()

    def is_read_by_user(self, user):
        return user in self.readers.all()

    def __str__(self):
        return f"{self.sender.username} in {self.group_chat.name} - {self.timestamp}"