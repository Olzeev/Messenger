import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        time = text_data_json['time']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                'type': 'chat_message', 
                'message': message, 
                'sender': 0,  
                'time': time
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        time = event['time']

        self.send(text_data=json.dumps({
            'type': 'chat', 
            'message': message, 
            'sender': 1, 
            'time': time
        }))