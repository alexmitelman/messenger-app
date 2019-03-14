from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Message, Chat
import json


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        contact_name = self.scope['url_route']['kwargs']['contact_name']
        current_username = self.scope['user'].username
        self.chat = Chat.get(current_username, contact_name)
        self.room_group_name = str(self.chat)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        self.send_history()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()
        sender = text_data_json['sender']
        sender_user = User.objects.filter(username=sender)[0]

        message_obj = Message.objects.create(
            sender=sender_user,
            content=message,
            chat=self.chat
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    def send_history(self):
        messages = Message.get_history(self.chat)
        for message in messages:
            message_json = self.message_to_json(message)
            message_json['type'] = 'chat_message'
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                message_json
            )

    def message_to_json(self, message):
        return {
            'sender': message.sender.username,
            'message': message.content,
            'timestamp': str(message.timestamp)
        }
