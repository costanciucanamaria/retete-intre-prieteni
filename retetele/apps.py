from django.apps import AppConfig


class ReteteleConfig(AppConfig):
    name = 'retetele'


    def ready(self):
        import retetele.signals