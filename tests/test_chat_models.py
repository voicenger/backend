import pytest
from django.utils import timezone
from voicengerapp.models import Chat, ChatParticipant, User

@pytest.mark.django_db
def test_chat_creation():
    chat = Chat.objects.create(description="Test chat")
    
    assert chat.description == "Test chat"
    assert chat.created_at is not None
    assert chat.updated_at is not None
    assert chat.is_archived is False
    assert chat.closed_at is None
    assert chat.last_message is None

@pytest.mark.django_db
def test_chatparticipant_creation():
    user = User.objects.create(username='testuser', email='testuser@example.com')
    chat = Chat.objects.create(description="Test chat")
    
    participant = ChatParticipant.objects.create(user=user, chat=chat)
    
    assert participant.user == user
    assert participant.chat == chat
    assert participant.joined_at is not None
    assert participant.is_admin is False
    assert participant.notifications_enabled is True

@pytest.mark.django_db
def test_unique_together_constraint():
    user = User.objects.create(username='testuser', email='testuser@example.com')
    chat = Chat.objects.create(description="Test chat")
    
    ChatParticipant.objects.create(user=user, chat=chat)
    
    with pytest.raises(Exception):
        # This should raise an exception because of the unique_together constraint
        ChatParticipant.objects.create(user=user, chat=chat)

@pytest.mark.django_db
def test_chat_is_archived():
    chat = Chat.objects.create(description="Test chat", is_archived=True)
    
    assert chat.is_archived is True
