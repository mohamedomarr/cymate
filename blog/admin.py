from django.contrib import admin
from .models import User, Post, Comment, Profile, Reacts, Share, Notification
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Reacts)
admin.site.register(Share)
admin.site.register(Notification)