from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Post, Comment, Profile, Reacts, Share, Notification

# Inline admin for Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('job_title', 'job_status', 'brief', 'years_of_experience', 'profile_image', 'phone_number')

# Register User model with proper admin interface
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'toolkit_tokens', 'profile_picture_preview', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [ProfileInline]
    
    # Add toolkit_tokens to the fieldsets for editing
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Toolkit', {'fields': ('toolkit_tokens',)}),
    )
    
    def profile_picture_preview(self, obj):
        """Display profile picture thumbnail in admin list"""
        try:
            if hasattr(obj, 'user_profile') and obj.user_profile.profile_image:
                return format_html(
                    '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                    obj.user_profile.profile_image.url
                )
            return "No Image"
        except:
            return "No Profile"
    
    profile_picture_preview.short_description = 'Profile Picture'

# Register Profile model with enhanced admin interface
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'job_status', 'years_of_experience', 'profile_image_preview')
    list_filter = ('job_status', 'years_of_experience')
    search_fields = ('user__username', 'user__email', 'job_title')
    raw_id_fields = ('user',)
    
    def profile_image_preview(self, obj):
        """Display profile image thumbnail in admin list"""
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_image.url
            )
        return "No Image"
    
    profile_image_preview.short_description = 'Profile Image'

# Register other models with basic admin interface
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reacts)
admin.site.register(Share)
admin.site.register(Notification)