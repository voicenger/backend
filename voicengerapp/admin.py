from django.contrib import admin

from .models import Chat, Message, UserChat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    search_fields = ('participants__username',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'text')
    list_filter = ('is_read', 'timestamp')


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'last_read_message')
    search_fields = ('user__username', 'chat__id')
    list_filter = ('chat',)
