# consumers.py

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

class TicksSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        # Get group_code from the URL
        group_code = self.scope['url_route']['kwargs']['group_code']
        
        # Accept the WebSocket connection
        self.send({
            'type': 'websocket.accept'
        })

        # Join the group based on group_code
        async_to_sync(self.channel_layer.group_add)(
            group_code,  # Use group_code as the group name
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Get group_code from the URL
        group_code = self.scope['url_route']['kwargs']['group_code']
        
        # Leave the group when disconnected
        async_to_sync(self.channel_layer.group_discard)(
            group_code,  # Use group_code as the group name
            self.channel_name
        )

    def new_ticks(self, event):
        # Send the new ticks data to the WebSocket client
        self.send({
            'type': 'websocket.send',
            'text': event['content'],  # Data you want to send
        })
