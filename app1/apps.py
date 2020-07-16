from django.apps import AppConfig


class App1Config(AppConfig):
    name = 'app1'

    def ready(self):

        from app1 import app1Updater
        app1Updater.start()