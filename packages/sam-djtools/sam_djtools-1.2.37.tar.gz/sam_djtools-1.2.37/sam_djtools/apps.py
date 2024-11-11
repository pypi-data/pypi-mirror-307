from django.conf import settings
from django.apps import AppConfig


class SamToolsConfig(AppConfig):
    name = 'sam_djtools'

    def ready(self):
        settings.MIDDLEWARE = ['django_currentuser.middleware.ThreadLocalUserMiddleware'] + settings.MIDDLEWARE
