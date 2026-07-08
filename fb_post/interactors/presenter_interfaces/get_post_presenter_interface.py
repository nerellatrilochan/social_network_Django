import abc

from django.http import HttpResponse

from fb_post.interactors.storage_interfaces.dtos import PostDetailsDTO


class GetPostPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_post_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def get_get_post_response(
        self, post_details_dto: PostDetailsDTO,
    ) -> HttpResponse:
        pass