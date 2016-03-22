from django.apps import AppConfig


class TextFormatConfig(AppConfig):
    name = 'django_textformat'

    def ready(self):
        from .signal_handlers import setup
        from .registry import registry

        setup()
        registry.autoload()
