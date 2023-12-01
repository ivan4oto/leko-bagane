from activity_services.update_activity import update_activity
from models.athlete_activity import AthleteActivity
from models.strava_wh_event import StravaWhEvent


class EventHandlingService():
    def __init__(self) -> None:
        pass

    async def handle_event(self, event: StravaWhEvent):
        if event.aspect_type == 'create' and event.object_type == 'activity':
            activity = await AthleteActivity.filter(activity_id = event.object_id).first()
            if activity is None:
                await AthleteActivity.create(
                    activity_id=event.object_id,
                    athlete_id = event.owner_id,
                    name = "",
                    description = ""
                    )

            # result = get_strava_activity(id=event.object_id)
            await update_activity(event.owner_id, event.object_id, name='UPDATED NAME', description='UPDATED DESCRIPTION')
            # return result