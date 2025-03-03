import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import ChatMessage as Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["url_route"]["kwargs"]["sender"]
        self.recipient = self.scope["url_route"]["kwargs"]["recipient"]
        self.room_group_name = f"chat_{min(self.sender, self.recipient)}_{max(self.sender, self.recipient)}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_previous_messages()
        await self.send(text_data=json.dumps({"previous_messages": messages}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            sender = data.get("sender")
            recipient = data.get("recipient")

            if not message or not sender or not recipient:
                return

            await self.save_message(sender, recipient, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                    "recipient": recipient,
                }
            )
        except json.JSONDecodeError:
            print("Error decoding JSON")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "recipient": event["recipient"],
        }))

    @database_sync_to_async
    def get_previous_messages(self):
        messages = Message.objects.filter(
            sender__username__in=[self.sender, self.recipient],
            recipient__username__in=[self.sender, self.recipient]
        ).order_by("-timestamp")[:20].values("sender__username", "message")
        return list(messages)

    @database_sync_to_async
    def save_message(self, sender, recipient, message):
        sender_user = User.objects.get(username=sender)
        recipient_user = User.objects.get(username=recipient)
        msg = Message.objects.create(sender=sender_user, recipient=recipient_user, message=message)
        print(f"Message saved: {msg}")
