from django.apps import AppConfig

class PostsAppConfig(AppConfig):
    name = "posts"

    def ready(self):
        # ruff: noqa: F401
        # pylint: disable=W0611
        from posts import signals # pylint: disable=unused-variable
