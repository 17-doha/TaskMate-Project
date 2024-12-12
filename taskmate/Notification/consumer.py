from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer():
    async def connect(self):
        self.group_name = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
#this funciton called when the message became in the channel layer   y3ne lama el message user a yb3atha btro7 ll channel el websocket bya5odha w yb3atha ll user
    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))