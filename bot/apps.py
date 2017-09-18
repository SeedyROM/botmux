from django.apps import AppConfig


class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        from . import signals
        # from . import jobs
