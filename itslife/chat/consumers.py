import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import Message, Room
from users.models import User

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user1 = self.scope.get('user')
        await self.accept()
        self.other_user = self.scope['url_route']['kwargs']['user_id'] 
        self.user2 = await sync_to_async(User.objects.get)(id=self.other_user)
        self.room = await sync_to_async(Room.objects.get_or_create)(user1=self.user1, user2=self.user2)
        self.room_name = f'Room {self.room.id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, data):
        text = data.get('message')
        self.message = await sync_to_async(Message.objects.create)(text=text, sender = self.user1, room = self.room)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "message",
                "id": self.message.id,
                "text": text,
                "sender": self.message.sender,
                "profile_pic": self.message.sender.profile_pic
            }
        )

    async def chat_messages(self, event):
        await self.send_json({
            "id": event['id'],
            "text": event['text'],
            "sender": event['sender'],
            "profile_pic": event['profile_pic']
        })

    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )