from django.contrib import admin
from .models import Announcementss, Comment, AnnouncementPermission
admin.site.register(Announcementss)
admin.site.register(Comment)
admin.site.register(AnnouncementPermission)