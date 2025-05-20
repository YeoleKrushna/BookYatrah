import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage
from exchanges.models import ExchangeRequest
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.exchange_id = self.scope['url_route']['kwargs']['exchange_id']
        self.room_group_name = f'chat_{self.exchange_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        # Save message in DB
        exchange = await database_sync_to_async(ExchangeRequest.objects.get)(id=self.exchange_id)
        await database_sync_to_async(ChatMessage.objects.create)(
            exchange=exchange,
            sender=user,
            message=message
        )

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': user.username,
                'sender_id': user.id,
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
