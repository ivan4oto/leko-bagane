from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel


class StravaWhEvent(Model):
    aspect_type = fields.CharField(50)
    event_time = fields.IntField()
    object_id = fields.IntField()
    object_type = fields.CharField(50)
    owner_id = fields.IntField()
    subscription_id = fields.IntField()
    updates = fields.JSONField()


class StravaWhEventIn(BaseModel):
    aspect_type: str
    event_time: int
    object_id: int
    object_type: str
    owner_id: int
    subscription_id: int
    updates: dict