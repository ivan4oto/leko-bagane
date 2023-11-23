from tortoise import fields
from tortoise.models import Model

class Athlete(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
