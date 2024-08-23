import pytest
from datetime import datetime, timezone, timedelta
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from voicengerapp.models import Chat, Message
from voicengerapp.consumers.chat_consumer import ChatConsumer
from channels.db import database_sync_to_async

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_chats():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser',
        password='password123'
    )
    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user)

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({'type': 'getChats'})
    response = await communicator.receive_json_from()
    assert response['type'] == 'chatsList'
    assert 'data' in response
    chats = response['data']
    assert isinstance(chats, list)
    assert len(chats) > 0

    first_chat = chats[0]
    assert 'id' in first_chat
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_chat_detail():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser1',
        password='password123'
    )
    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user)

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()

    assert connected

    await (communicator.send_json_to({
            'type': 'getChatDetails',
            'data': {
                'chatId': chat.id
            }
        })
    )
    response = await communicator.receive_json_from()

    assert response['type'] == 'chatDetails'
    assert 'data' in response
    chat_details = response['data']
    assert chat_details['id'] == chat.id
    assert len(chat_details['participants']) == 1
    assert chat_details['participants'][0]['username'] == 'testuser1'

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_create_empty_chat():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser2',
        password='password123'
    )

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected

    chat_data = {
        'type': 'createEmptyChat',
        'data': {}
    }

    await communicator.send_json_to(chat_data)
    response = await communicator.receive_json_from()

    assert response['type'] == 'emptyChatCreated'

    assert 'data' in response
    data = response['data']

    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    assert data['id'] is not None
    assert 'created_at' in data
    assert 'updated_at' in data

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_join_chat():
    user1 = await database_sync_to_async(get_user_model().objects.create_user)(
        username='testuser3',
        password='password123'
    )
    user2 = await database_sync_to_async(get_user_model().objects.create_user)(
        username='testuser4',
        password='password123'
    )

    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user1)

    last_message = await database_sync_to_async(Message.objects.create)(
        chat=chat,
        sender=user1,
        text='Hello World!',
        timestamp=datetime.now(timezone.utc)
    )

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user2
    connected, _ = await communicator.connect()
    assert connected

    join_chat_data = {
        'type': 'joinChat',
        'data': {
            'chat': chat.id,
            'last_read_message': None,
        }
    }

    await communicator.send_json_to(join_chat_data)
    response = await communicator.receive_json_from()

    assert response['type'] == 'chatJoined'

    assert 'data' in response
    assert 'chat' in response['data']
    assert 'user' in response['data']
    assert 'last_read_message' in response['data']
    assert response['data']['chat'] == chat.id
    assert response['data']['user']['id'] == user2.id
    assert response['data']['user']['username'] == user2.username
    assert response['data']['last_read_message'] == last_message.id

    is_participant = await database_sync_to_async(chat.participants.filter(id=user2.id).exists)()
    assert is_participant

    await communicator.send_json_to(join_chat_data)
    response = await communicator.receive_json_from()

    assert response['type'] == 'info'
    assert 'message' in response
    assert response['message'] == 'You are already a participant in this chat.'

    join_chat_data_invalid_chat = {
        'type': 'joinChat',
        'data': {
            'chat': 9999,
        }
    }
    await communicator.send_json_to(join_chat_data_invalid_chat)
    response_invalid_chat = await communicator.receive_json_from()

    # Check that the response indicates the chat was not found
    assert response_invalid_chat['type'] == 'error'
    assert 'message' in response_invalid_chat
    assert response_invalid_chat['message'] == 'Chat not found.'
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_create_new_message_success():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser22',
        password='password123'
    )

    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user)

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected

    message_data = {
        'type': 'newMessage',
        'data': {
            'chat': chat.id,
            'text': 'Hello World!',
        }
    }

    await communicator.send_json_to(message_data)
    response = await communicator.receive_json_from()

    assert response['type'] == 'messageCreated'
    assert 'data' in response

    message = response['data']
    assert 'id' in message
    assert 'chat' in message
    assert 'sender' in message
    assert 'text' in message
    assert 'timestamp' in message
    assert 'is_read' in message
    assert message['text'] == 'Hello World!'
    assert message['sender']['id'] == user.id
    assert message['sender']['username'] == user.username
    assert message['is_read'] == False

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_unauthenticated_user():
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    connected, _ = await communicator.connect()
    assert not connected
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_chat_messages():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser0001111',
        password='password123'
    )
    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user)

    now = datetime.now(timezone.utc)
    timestamp1 = now - timedelta(days=3)
    timestamp2 = now - timedelta(days=1, hours=2)
    timestamp3 = now - timedelta(hours=1)

    message1 = await database_sync_to_async(Message.objects.create)(
        chat=chat, sender=user, text="Message 1", timestamp=timestamp1
    )
    message2 = await database_sync_to_async(Message.objects.create)(
        chat=chat, sender=user, text="Message 2", timestamp=timestamp2
    )
    message3 = await database_sync_to_async(Message.objects.create)(
        chat=chat, sender=user, text="Message 3", timestamp=timestamp3
    )

    assert message1.timestamp == timestamp1, f"Expected: {timestamp1}, but got: {message1.timestamp}"
    assert message2.timestamp == timestamp2, f"Expected: {timestamp2}, but got: {message2.timestamp}"
    assert message3.timestamp == timestamp3, f"Expected: {timestamp3}, but got: {message3.timestamp}"

    print(f"Message 1 timestamp: {message1.timestamp}")
    print(f"Message 2 timestamp: {message2.timestamp}")
    print(f"Message 3 timestamp: {message3.timestamp}")

    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected


    await communicator.send_json_to({
        "type": "getChatMessages",
        "data": {
            "chatId": chat.id,
            "date_from": "yesterday"
        }
    })

    response = await communicator.receive_json_from()
    assert response['type'] == 'chatMessages'
    assert len(response['data']) == 2

    await communicator.send_json_to({
        "type": "getChatMessages",
        "data": {
            "chatId": chat.id,
            "last": 1
        }
    })

    response = await communicator.receive_json_from()
    assert response['type'] == 'chatMessages'
    assert len(response['data']) == 1

    await communicator.disconnect()