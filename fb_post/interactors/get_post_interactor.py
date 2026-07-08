from fb_post.exceptions.custom_exceptions import InvalidPostException
from fb_post.interactors.presenter_interfaces.get_post_presenter_interface import (
    GetPostPresenterInterface,
)
from fb_post.interactors.storage_interfaces.dtos import PostDetailsDTO
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)


class GetPostInteractor:

    def __init__(self, post_storage: PostStorageInterface):
        self.post_storage = post_storage

    def get_post_wrapper(
        self,
        post_id: int,
        presenter: GetPostPresenterInterface,
    ):
        try:
            post_details_dto = self.get_post(post_id=post_id)
        except InvalidPostException:
            return presenter.raise_invalid_post_exception()

        return presenter.get_get_post_response(
            post_details_dto=post_details_dto,
        )

    def get_post(self, post_id: int) -> PostDetailsDTO:
        """
        Fetches full post details including comments, reactions, and replies.

        Raises:
            InvalidPostException: when post does not exist
        """
        return self.post_storage.get_post_details(post_id=post_id)