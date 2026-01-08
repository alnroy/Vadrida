# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from coreapi.models import UserProfile # Import User from coreapi
from .models import ChatMessage       # Import ChatMessage from local app

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat"
        self.user = await self.get_user_from_session()

        if self.user:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if not self.user: return

        # Save to DB
        saved_msg = await self.save_message(
            data.get('content', ''),
            data.get('attached_type', 'none'),
            data.get('attached_path'),
            data.get('attached_label')
        )

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': saved_msg.id,
                'user': self.user.user_name,
                'content': saved_msg.content,
                'attached_type': saved_msg.attached_type,
                'attached_path': saved_msg.attached_path,
                'attached_label': saved_msg.attached_label,
                'time': saved_msg.created_at.strftime("%H:%M")
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user_from_session(self):
        session = self.scope.get("session")
        if not session or "user_id" not in session: return None
        try: return UserProfile.objects.get(id=session["user_id"])
        except UserProfile.DoesNotExist: return None

    @database_sync_to_async
    def save_message(self, content, att_type, path, label):
        return ChatMessage.objects.create(
            user=self.user, content=content,
            attached_type=att_type, attached_path=path, attached_label=label
        )