from django.contrib import admin
from .models import User, Chat, ChatParticipant, Message, MessageReadReceipt

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(ChatParticipant)
admin.site.register(Message)
admin.site.register(MessageReadReceipt)