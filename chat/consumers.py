"""
A channel layer is a kind of communication system. It allows multiple
consumer instance to talk with each other and with other parts of Django.
A channel layer provides the following abstractions:
1. A channel is a mailbox where messages can be sent to. Each channel has
a name. Anyone who has the name of the a channel can send a message to the
channel.
2. A group is a group of related channels. A group has a name. Anyone who has
the name of a group can add/remove a channel to the group by name and send a
message to all channels in the group. It is not possible to enumerate what
channels are in a particular group.
Every consumer instance has an automatically generated unique channel name
and so can be communicated with via a channel layer.
In our chat application we want to have multiple instances of a ChatConsumer
in the same room communicating with each other. To do that we will have each
ChatConsumer add its channel to a group whose name is based on the room name.
That will allow ChatConsumers to transmit messages to all other ChatConsumers
in the same room.

When a user posts a message, a JavaScript function will transmit the message
over Websocket to a ChatConsumer. The chatconsumer will receive that message
and forward it to the group corresponding to the room name. Every chatConsumer
in the same group(and thus in the same room) will then receive the message
from the group and forward it over WebSocket back to Javascript where it
will be appended to the chat log.
"""

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """
    This is a synchronous websocket consumer that
    accepts all connections, receives messages from
    its client and echoes those messages back to the
    same client
    channels also supports writing asynchronous consumer
    for greater performance. However any asynchronous
    consumer must be careful to avoid directly performing
    bocking operations, such as accessing a Django model
    """
    """
    All channel layer methods are asynchronous. Therefore
    we have to use the async_to_sync wrapper.
    """

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print(self.room_group_name)
        print(self.channel_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from websocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f'message {message} received')
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(f'Inside chat_message method, message is {message}')

        # send message to websocket
        self.send(text_data=json.dumps({
            'message': message
        }))