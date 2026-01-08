from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):  # <--- Changed this line
    # What columns to show in the list
    list_display = ('id', 'get_user', 'short_content', 'attached_type', 'is_pinned', 'created_at')
    
    # Add filters on the right side
    list_filter = ('is_pinned', 'attached_type', 'created_at')
    
    # Add a search bar
    search_fields = ('user__user_name', 'content', 'attached_label')
    
    # Make the list clickable
    list_display_links = ('id', 'short_content')

    # Helper to show user name
    def get_user(self, obj):
        return obj.user.user_name
    get_user.short_description = 'User'

    # Helper to truncate long messages
    def short_content(self, obj):
        if obj.content:
            return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
        return "(No Text)"
    short_content.short_description = 'Message'