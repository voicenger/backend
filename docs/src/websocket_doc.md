
# WebSocket API Documentation

## Table of Contents
- [getChats](#getChats)
- [createEmptyChat](#createEmptyChat)
- [joinChat](#joinChat)
- [getChatDetails](#getChatDetails)
- [newMessage](#newMessage)
- [getChatMessages](#getChatMessages)

---

## getChats

### Description:
Retrieve all chats in which the user participates.

### Request:

```json
{
  "type": "getChats",
  "data": {}
}
```

### Response:

```json
{
  "type": "chatsList",
  "data": [
    {
      "id": "int",                // chat ID
      "participants": [
        {
          "id": "int",            // participant ID
          "username": "string"    // Member user name
        }
      ],
      "created_at": "string",     // Date and time of chat creation
      "updated_at": "string"      // Date and time of the last chat update
    }
  ]
}
```

---

## createEmptyChat

### Description:
Create an empty chat entity, with no participants. The server creates a new chat and returns its identifier, as well as the timestamps of creation and last update.

### Request:

```json
{
  "type": "createEmptyChat",
  "data": {}
}
```

### Response:

```json
{
  "type": "emptyChatCreated",
  "data": {
    "id": "int",                 // New chat ID
    "participants": [],          // List of participants
    "created_at": "string",      // Date and time of chat creation
    "updated_at": "string"       // Date and time of the last chat update
  }
}
```

---

## joinChat

### Description:
Add the current user to an existing chat room. Optionally specify the ID of the last read message so that the server knows when to count new messages for this user.

### Request:

```json
{
  "type": "joinChat",
  "data": {
    "chat": "int",                 // ID of the chat room the user is joining
    "last_read_message": "int"     // ID of the last read message (optional)
  }
}
```

### Response:

```json
{
  "type": "chatJoined",
  "data": {
    "chat": "int",                 // ID of the chat room the user has joined
    "user": {
      "id": "int",                 // user ID
      "username": "string"         // User Name
    },
    "last_read_message": "int"     // ID of the last read message (if specified)
  }
}
```

---

## getChatDetails

### Description:
Get detailed information about a specific chat, including all participants, creation date, and last update date.

### Request:

```json
{
  "type": "getChatDetails",
  "data": {
    "chatId": "int"  // chat ID
  }
}
```

### Response:

```json
{
  "type": "chatDetails",
  "data": {
    "id": "int",                 // chat ID
    "participants": [
      {
        "id": "int",             // participant ID
        "username": "string"     // Member user name
      },
      {
        "id": "int",             // participant ID
        "username": "string"     // Member user name
      }
    ],
    "created_at": "string",      // Date and time of chat creation
    "updated_at": "string"       // Date and time of the last chat update
  }
}
```

---

## newMessage

### Description:
Send a new message to the specified chat room.

### Request:

```json
{
  "type": "newMessage",
  "data": {
    "chat": "int",           // ID of the chat room to which the message is sent
    "text": "string",        // Message Text
    "is_read": "boolean"     // // Message read status (optional, defaults to False if not provided)
  }
}
```

### Response:

```json
{
  "type": "messageCreated",
  "data": {
    "id": "int",             // ID of the created message
    "chat": "int",           // ID of the chat to which the message belongs
    "sender": {
      "id": "int",           // sender ID
      "username": "string"   // Sender's user name
    },
    "text": "string",        // Message Text
    "timestamp": "string",   // Time stamp for sending a message
    "is_read": "boolean"     // Message read status
  }
}
```

---

## getChatMessages

### Description:
Retrieve all messages in the specified chat room. Optionally filter messages by date or limit the number of last messages.

### Request:

```json
{
  "type": "getChatMessages",
  "data": {
    "chatId": "int",             // ID of the chat for which you want to retrieve messages
    "date_from": "string",       // Start date (YYYY-MM-DD) or special values: "yesterday", "day_before_yesterday", "last_7_days" (optional)
    "date_to": "string",         // End date (YYYY-MM-DD) (optional)
    "last": "int"                // Number of last messages to receive (optional)
  }
}
```

### Response:

```json
{
  "type": "chatMessages",
  "data": [
    {
      "id": "int",               // message ID
      "chat": "int",             // ID of the chat to which the message belongs
      "sender": {
        "id": "int",             // sender ID
        "username": "string"     // Sender's user name
      },
      "text": "string",          // Message Text
      "timestamp": "string",     // Time stamp for sending a message
      "is_read": "boolean"       // Message read status
    }
  ]
}
```
