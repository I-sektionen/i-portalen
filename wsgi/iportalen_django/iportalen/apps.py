from django.apps import AppConfig
from django.conf import settings
from utils.grunt import GruntProcess


class IportalenAppConfig(AppConfig):
    name = 'iportalen'
    verbose_name = 'I-Portalen'

    def ready(self):
        if settings.RUN_GRUNT:
            g = GruntProcess()
            g.start_grunt()
