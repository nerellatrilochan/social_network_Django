from django.apps import AppConfig


class FbPostAppConfig(AppConfig):
    name = "fb_post"

    def ready(self):
        from fb_post import signals # pylint: disable=unused-variable
