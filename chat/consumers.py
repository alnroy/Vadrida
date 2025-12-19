# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import UserProfile
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "global"
        self.room_group_name = f"chat_{self.room_name}"

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

        
    async def receive(self, text_data):
        data = json.loads(text_data)

        user = await sync_to_async(UserProfile.objects.get)(
            user_name=data["user"]
        )

        msg = await sync_to_async(ChatMessage.objects.create)(
            user=user,
            content=data.get("content", ""),
            message_type=data.get("attached_type", "text"),
            file_path=data.get("attached_path")
        )

        payload = {
            "user": user.user_name,
            "content": msg.content,
            "time": msg.created_at.strftime("%H:%M"),
            "attached_type": data.get("attached_type"),
            "attached_path": data.get("attached_path"),
            "attached_label": data.get("attached_label"),
        }

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_message",
                **payload
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_message(self, data):
        """Save message to database and return serialized data"""
        user = self.scope["user"]
        
        # Get user profile - adjust based on your User model structure
        try:
            user_profile = user.user_profile
            username = user_profile.user_name
        except AttributeError:
            username = user.username
        
        msg = ChatMessage.objects.create(
            user=user_profile if hasattr(user, 'user_profile') else user,
            content=data.get("content", ""),
            attached_type=data.get("attached_type", "none"),
            attached_path=data.get("attached_path"),
            attached_label=data.get("attached_label"),
            is_pinned=data.get("pin", False)
        )
        
        return {
            "id": msg.id,
            "user": username,
            "content": msg.content,
            "attached_type": msg.attached_type,
            "attached_path": msg.attached_path,
            "attached_label": msg.attached_label,
            "is_pinned": msg.is_pinned,
            "time": msg.created_at.strftime("%H:%M")
        }