from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Message
import json


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.contact_name = self.scope['url_route']['kwargs']['contact_name']
        self.room_group_name = 'chat_%s' % self.contact_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

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
