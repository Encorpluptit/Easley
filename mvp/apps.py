from django.apps import AppConfig


class MvpConfig(AppConfig):
    name = 'mvp'

    def ready(self):
        import mvp.signals
        import mvp.templatetags
