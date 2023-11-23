from tortoise import fields
from tortoise.models import Model

class AthleteActivity(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    description = fields.TextField()
    is_updated = fields.BooleanField(default=False)
