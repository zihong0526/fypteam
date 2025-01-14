from django.contrib import admin
from .models import Message
from .models import GroupChat, GroupMessage
admin.site.register(Message)
admin.site.register(GroupChat)
admin.site.register(GroupMessage)
