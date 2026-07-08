from fb_post.exceptions.custom_exceptions import (
    InvalidPostContent,
    InvalidUserException,
)
from fb_post.interactors.presenter_interfaces.create_post_presenter_interface import (
    CreatePostPresenterInterface,
)
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)


class CreatePostInteractor:

    def __init__(self, post_storage: PostStorageInterface):
        self.post_storage = post_storage

    def create_post_wrapper(
        self,
        user_id: int,
        post_content: str,
        presenter: CreatePostPresenterInterface,
    ):
        try:
            post_id = self.create_post(
                user_id=user_id,
                post_content=post_content,
            )
        except InvalidUserException:
            return presenter.raise_invalid_user_exception()
        except InvalidPostContent:
            return presenter.raise_invalid_post_content_exception()

        return presenter.get_create_post_response(post_id=post_id)

    def create_post(self, user_id: int, post_content: str) -> int:
        """
        Validates and creates a post.

        Raises:
            InvalidUserException: when user does not exist
            InvalidPostContent: when post content is empty or whitespace
        """
        if not self.post_storage.does_user_exist(user_id=user_id):
            raise InvalidUserException

        if not post_content or not post_content.strip():
            raise InvalidPostContent

        return self.post_storage.create_post(
            user_id=user_id,
            post_content=post_content,
        )