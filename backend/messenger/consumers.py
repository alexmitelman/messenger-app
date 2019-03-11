from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
import json


user = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))