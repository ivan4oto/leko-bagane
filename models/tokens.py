from tortoise.models import Model
from tortoise import fields

class RefreshToken(Model):
    id = fields.IntField(pk=True)
    token = fields.TextField()
    athlete = fields.ForeignKeyField('models.Athlete', related_name='refresh_tokens')
    expires = fields.DatetimeField()
