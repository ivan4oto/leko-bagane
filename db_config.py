TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:postgres@db/lekobagane"},
    "apps": {
        "models": {
            "models": [
                "models.athlete",
                "models.athlete_activity",
                "models.strava_wh_event",
                "models.webhook_validator",
                "models.tokens"
                ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}