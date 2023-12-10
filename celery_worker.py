from celery import Celery
from activity_services.get_activity import fetch_activity

from activity_services.update_activity import update_activity
from decorators.async_to_sync import async_task


celery_app = Celery(__name__)
celery_app.conf.broker_url = "redis://localhost:6379"
celery_app.conf.result_backend = "redis://localhost:6379"


@async_task(celery_app)
async def update_athlete_activity_task(
    activity_id: str,
    name: str,
    description: str
    ):
    activity = await fetch_activity(activity_id)
    await update_activity(activity, name, description)
