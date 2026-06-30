from django.apps import AppConfig


class PostsAuthAppConfig(AppConfig):
    name = "users"

    def ready(self):
        # ruff: noqa: F401
        # pylint: disable=W0611
        from posts_auth import signals # pylint: disable=unused-variable
