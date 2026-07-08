import abc

from django.http import HttpResponse


class ReactToPostPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_user_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_post_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_reaction_type_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def get_react_to_post_response(self) -> HttpResponse:
        pass