import abc

from django.http import HttpResponse


class CreatePostPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_user_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_post_content_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def get_create_post_response(self, post_id: int) -> HttpResponse:
        pass