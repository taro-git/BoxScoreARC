from django.apps import AppConfig
import os

class RestApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_api'

    def ready(self):
        # if os.environ.get('RUN_MAIN') != 'true':
        #     return
        print(f'called RestApiConfig.ready: worker pid = {os.getpid()}')
        from rest_api.core.schedulers import start_scheduler
        start_scheduler()
