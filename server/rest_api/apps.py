from django.apps import AppConfig

from box_score_arc.settings import is_db_manage_mode


class RestApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rest_api"

    def ready(self):
        from rest_api.jobs import signals  # noqa : F401

        if is_db_manage_mode:
            from rest_api.core.schedulers import start_scheduler

            start_scheduler()
