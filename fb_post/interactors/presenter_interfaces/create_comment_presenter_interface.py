import abc

from django.http import HttpResponse


class CreateCommentPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_user_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_post_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_comment_content_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def get_create_comment_response(self, comment_id: int) -> HttpResponse:
        pass