import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # default notification (by3mel group l kol user yb3at 3aleh el notification)
        self.user_id = self.scope['user'].id
        self.group_name = f"user_{self.user_id}"  # Group name unique to user ID

        #by7ot el group 3la el channel f kda el websocket done ll users elly fel group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"User {self.user_id} connected to WebSocket group {self.group_name}")

    async def disconnect(self, close_code):
        #b shelhom men el channel
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"User {self.user_id} disconnected")

    async def send_notification(self, event):
        # Send the notification message
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
