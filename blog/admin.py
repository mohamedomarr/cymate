from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Post, Comment, Profile, Reacts, Share, Notification

# Register User model with proper admin interface
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register other models
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Reacts)
admin.site.register(Share)
admin.site.register(Notification)