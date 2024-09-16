import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .timescale_db import get_latest_power_readings


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class PowerReadingsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_latest_readings(self, sensor_id):
        return get_latest_power_readings(sensor_id, 100)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sensor_id = data.get("sensor_id")
        if sensor_id:
            readings = await self.get_latest_readings(sensor_id)
            await self.send(
                text_data=json.dumps({"readings": readings}, cls=DateTimeEncoder)
            )
