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
"""

import json
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
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))