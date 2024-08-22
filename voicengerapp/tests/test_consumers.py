import pytest
from django.contrib.auth import get_user_model

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

    await communicator.send_json_to({'command': 'getChats'})
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

    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected

    # Send a command to get chat details
    await communicator.send_json_to({
        'command': 'getChatDetails',
        'chat_id': chat.id
    })

    # Receive the response
    response = await communicator.receive_json_from()

    # Assert the response
    assert response['type'] == 'chatDetails'
    assert 'data' in response
    chat_details = response['data']
    assert chat_details['id'] == chat.id
    assert len(chat_details['participants']) == 1
    assert chat_details['participants'][0]['username'] == 'testuser1'

    # Disconnect from the WebSocket
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_create_chat():
    user = await database_sync_to_async(User.objects.create_user)(
        username='testuser2',
        password='password123'
    )
    # Set up a WebSocket connection and authenticate the user
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected

    # Data for creating a new chat
    chat_data = {
        'command': 'createEmptyChat',
        'participants': [user.id],
    }
    # Send the data to create the chat and wait for a response
    await communicator.send_json_to(chat_data)
    response = await communicator.receive_json_from()

    assert response['type'] == 'emptyChatCreated'

    # Access 'data' key
    assert 'data' in response
    data = response['data']

    # Verify that all expected fields are present in the data
    assert 'id' in data
    assert 'participants' in data

    # Check the content of the chat
    assert data['id'] is not None
    assert len(data['participants']) == 1
    assert data['participants'][0]['id'] == user.id

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

    # Create a chat and add the first user as a participant
    chat = await database_sync_to_async(Chat.objects.create)()
    await database_sync_to_async(chat.participants.add)(user1)

    # Create a message in the chat
    last_message = await database_sync_to_async(Message.objects.create)(
        chat=chat,
        sender=user1,
        text='Hello World!',
        timestamp=datetime.now(timezone.utc)
    )

    # Set up WebSocket and authenticate the second user
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chats/")
    communicator.scope['user'] = user2
    connected, _ = await communicator.connect()
    assert connected

    # Data to join the chat
    join_chat_data = {
        'command': 'joinChat',
        'chat_id': chat.id,
    }

    # Send data to join the chat and receive the response
    await communicator.send_json_to(join_chat_data)
    response = await communicator.receive_json_from()

    # Check the type of response
    assert response['type'] == 'chatJoined'

    # Check the presence of 'data' in the response and its contents
    assert 'data' in response
    assert 'chat' in response['data']
    assert 'user' in response['data']
    assert 'last_read_message' in response['data']
    assert response['data']['chat'] == chat.id
    assert response['data']['user']['id'] == user2.id
    assert response['data']['user']['username'] == user2.username

    # Verify that last_read_message is returned correctly
    assert response['data']['last_read_message'] == last_message.id

    # Check if the user was successfully added to the chat
    is_participant = await database_sync_to_async(chat.participants.filter(id=user2.id).exists)()
    assert is_participant

    # Attempt to join the chat again to test handling of already joined users
    await communicator.send_json_to(join_chat_data)
    response = await communicator.receive_json_from()

    # Check that the response indicates the user is already in the chat
    assert response['type'] == 'info'
    assert 'message' in response
    assert response['message'] == 'You are already a participant in this chat.'

    # Test with an invalid chat ID to check error handling
    join_chat_data_invalid_chat = {
        'command': 'joinChat',
        'chat_id': 9999,
    }
    await communicator.send_json_to(join_chat_data_invalid_chat)
    response_invalid_chat = await communicator.receive_json_from()

    # Check that the response indicates the chat was not found
    assert response_invalid_chat['type'] == 'error'
    assert 'message' in response_invalid_chat
    assert response_invalid_chat['message'] == 'The chat you are trying to join does not exist.'
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
        'command': 'newMessage',
        'chat_id': chat.id,
        'text': 'Hello World!',
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

import pytest
from datetime import datetime, timedelta, timezone
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from voicengerapp.models import Chat, Message
from voicengerapp.consumers import ChatConsumer
from channels.db import database_sync_to_async

User = get_user_model()

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
        "command": "getChatMessages",
        "data": {
            "chatId": chat.id,
            "date_from": "yesterday"
        }
    })

    response = await communicator.receive_json_from()
    assert response['command'] == 'chatMessages'
    assert len(response['data']) == 2

    await communicator.send_json_to({
        "command": "getChatMessages",
        "data": {
            "chatId": chat.id,
            "last": 1
        }
    })

    response = await communicator.receive_json_from()
    assert response['command'] == 'chatMessages'
    assert len(response['data']) == 1

    await communicator.disconnect()