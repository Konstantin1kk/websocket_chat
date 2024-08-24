from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import json
from . import models


class WSConsumer(WebsocketConsumer):
    async def connect(self):
        self.roomGroupName = 'group_chat'

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chat_id']
        models.Message.objects.create(text=message, chat_id=chat_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendMessage',
                'message': message,
                'username': username,
            }
        )

    async def sendMessage(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({'message': message, 'username': username}))
