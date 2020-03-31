from django.apps import AppConfig


class TwitterappConfig(AppConfig):
    name = 'twitterapp'

    def ready(self):
    	import twitterapp.signals
