import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from views import GetId


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'global'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        time = text_data_json['time']
        id_sender = text_data_json['id_sender']
        id_reciever = text_data_json['id_reciever']
        
        id1 = GetId.get()
        if id_reciever == id1:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, 
                {
                    'type': 'chat_message', 
                    'message': message, 
                    'sender': 1,
                    'time': time
                }
            )
        elif id_sender == id1:
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
        id_sender = event['id_sender']
        id_reciever = event['id_reciever']

        self.send(text_data=json.dumps({
            'type': 'chat', 
            'message': message, 
            'id_sender': id_sender,
            'id_reciever': id_reciever,
            'time': time
        }))