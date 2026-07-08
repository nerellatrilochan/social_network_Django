import abc

from django.http import HttpResponse


class DeletePostPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_user_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_post_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_user_cannot_delete_post_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def get_delete_post_response(self) -> HttpResponse:
        pass