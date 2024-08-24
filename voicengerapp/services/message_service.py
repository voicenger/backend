from channels.db import database_sync_to_async
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta


class MessageService:
    """
    Service class for handling operations related to messages in a chat.
    """

    @database_sync_to_async
    def serialize_messages(self, messages):
        """
        Serializes a list of message objects for WebSocket transmission.
        """

        from voicengerapp.serializers import WebSocketMessageSerializer
        serializer = WebSocketMessageSerializer(messages, many=True)
        return serializer.data

    @database_sync_to_async
    def get_last_message(self, chat_id: id):
        """
        Retrieves the last message in a chat based on its timestamp.
        """

        from voicengerapp.models import Message
        try:
            last_message = Message.objects.filter(chat_id=chat_id).latest('timestamp')
            return last_message.id
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, chat_id: int, text: str, sender, is_read: bool):
        """
        Creates and saves a new message in the specified chat.
        """

        from voicengerapp.models import Message
        message = Message.objects.create(
            chat_id=chat_id,
            text=text,
            sender=sender,
            timestamp=timezone.now(),
            is_read=is_read
        )
        return message

    @database_sync_to_async
    def get_messages(self, chat_id, date_from=None, date_to=None, last=None):
        """
        Retrieves messages from a chat, with optional filtering by date range or limiting the number of messages.

        :param chat_id: The ID of the chat.
        :param date_from: Optional start date to filter messages.
        :param date_to: Optional end date to filter messages.
        :param last: Optional parameter to limit the number of returned messages.
        :return: A queryset of filtered messages.
        """
        from voicengerapp.models import Message
        messages = Message.objects.filter(chat_id=chat_id)

        if date_from:
            date_from = self.parse_custom_date(date_from)
            if date_from:
                messages = messages.filter(timestamp__date__gte=date_from)

        if date_to:
            date_to = parse_date(date_to)
            if date_to:
                messages = messages.filter(timestamp__date__lte=date_to)

        if last and str(last).isdigit():
            messages = messages.order_by('-timestamp')[:int(last)]

        return messages

    def parse_custom_date(self, date_str):
        """
        Parses a custom date string into a date object.
        """
        if date_str == 'yesterday':
            return datetime.now().date() - timedelta(days=1)
        elif date_str == 'day_before_yesterday':
            return datetime.now().date() - timedelta(days=2)
        elif date_str == 'last_7_days':
            return datetime.now().date() - timedelta(days=7)
        else:
            return parse_date(date_str)