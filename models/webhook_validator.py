from tortoise.models import Model
from tortoise import fields

class WebhookValidator(Model):
    hub_mode = fields.CharField(max_length=50)
    hub_challenge = fields.CharField(max_length=100)
    hub_verify_token = fields.CharField(max_length=100)

    class Meta:
        table = "webhook_validators"