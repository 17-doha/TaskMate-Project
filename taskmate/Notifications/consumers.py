import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # bygeeg el user elly 3amel login delwa2ty
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')  
        if not self.user_id:
            await self.close()  # Close the connection if user_id is missing
            return

        self.group_name = f"user_{self.user_id}"   # Group name unique to user ID
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: User {self.user_id}")

    async def disconnect(self, close_code):
                #b shelhom men el channel
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: User {self.user_id}")

    async def send_notification(self, event):
        # Send the notification message
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


