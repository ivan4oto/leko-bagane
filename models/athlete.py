from tortoise import fields
from tortoise.models import Model

class Athlete(Model):
    id = fields.IntField(pk=True)
    athlete_id = fields.BigIntField()
    first_name = fields.CharField(50)
    last_name = fields.CharField(50)
    sex = fields.CharField(50)
    city = fields.CharField(50)

async def get_athlete_by_id(athlete_id: int) -> Athlete:
    try:
        athlete = await Athlete.get(athlete_id=athlete_id)
        return athlete
    except Athlete.DoesNotExist:
        return None