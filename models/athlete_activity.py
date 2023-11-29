from tortoise import fields
from tortoise.models import Model

class AthleteActivity(Model):
    id = fields.IntField(pk=True)
    activity_id = fields.BigIntField()
    athlete_id = fields.BigIntField()
    name = fields.CharField(50)
    description = fields.TextField()
    is_updated = fields.BooleanField(default=False)
