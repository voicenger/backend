from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist


class ChatService:
    """
    Service class for handling chat-related operations.

    This class provides asynchronous methods to interact with the Chat model,
    including retrieving, creating, and modifying chat objects.
    """

    @staticmethod
    @database_sync_to_async
    def get_all_chats():
        """
        Retrieves all chat objects from the database.
        """
        from voicengerapp.models import Chat
        return Chat.objects.all()

    @staticmethod
    @database_sync_to_async
    def get_chat(chat_id: int):
        """
        Retrieves a chat object by its ID from the database.
        """
        from voicengerapp.models import Chat
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def serialize_chats(chats):
        """
        Serializes the list of chat objects into a list of dictionaries.
        """
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chats, many=True)
        return serializer.data

    @staticmethod
    @database_sync_to_async
    def serialize_chat(chat):
        """
        Serializes a single chat object into a dictionary.
        """
        from voicengerapp.serializers import ChatSerializer
        serializer = ChatSerializer(chat)
        return serializer.data

    @staticmethod
    @database_sync_to_async
    def create_chat():
        """
        Create a new chat.
        """
        from voicengerapp.models import Chat
        chat = Chat.objects.create()
        return chat

    @staticmethod
    @database_sync_to_async
    def add_participants_to_chat(chat_id: int, participants_ids: list[int]):
        """
        Adds participants to a chat.
        """
        from voicengerapp.models import Chat
        from django.contrib.auth.models import User
        try:
            chat = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return {'error': 'Chat not found'}

        for participant_id in participants_ids:
            try:
                user = User.objects.get(id=participant_id)
                chat.participants.add(user)
            except ObjectDoesNotExist:
                continue
        chat.save()
        return chat

    @database_sync_to_async
    def is_user_in_chat(self, user, chat):
        """
        Checks if a user is a participant in a given chat.
        """
        return chat.participants.filter(id=user.id).exists()
