from datetime import datetime
from typing import Any


class BaseMessage:
    def __init__(self, message_type: str, data: Any):
        self.type = message_type
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the message object into a dictionary that can be serialized to JSON.
        """
        return {
            "type": self.type,
            "data": self.data
        }


class GetChatsMessage(BaseMessage):
    def __init__(self, serialized_chats: list[dict[str, Any]]):
        super().__init__("chatsList", serialized_chats)


class GetChatDetailsMessage(BaseMessage):
    def __init__(self, serialized_chat: dict[str, Any]):
        super().__init__("chatDetails", serialized_chat)


class CreateEmptyChatMessage(BaseMessage):
    def __init__(self, chat_id: int, participants: list[int], created_at: datetime, updated_at: datetime):
        data = {
            "id": chat_id,
            "participants": participants,
            "created_at": created_at,
            "updated_at": updated_at
        }
        super().__init__("emptyChatCreated", data)


class JoinChatMessage(BaseMessage):
    def __init__(self, chat_id: int, last_read_message=None, last_message=None):
        data = {
            "chat": chat_id
        }
        if last_read_message is not None:
            data["last_read_message"] = last_read_message
        if last_message is not None:
            data["last_message"] = last_message
        super().__init__("joinChat", data)
