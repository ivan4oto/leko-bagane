from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel


class StravaWhEvent(Model):
    aspect_type = fields.CharField(50)
    event_time = fields.BigIntField()
    object_id = fields.BigIntField()
    object_type = fields.CharField(50)
    owner_id = fields.BigIntField()
    subscription_id = fields.BigIntField()
    updates = fields.JSONField()


class StravaWhEventIn(BaseModel):
    aspect_type: str
    event_time: int
    object_id: int
    object_type: str
    owner_id: int
    subscription_id: int
    updates: dict