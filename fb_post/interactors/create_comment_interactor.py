from fb_post.exceptions.custom_exceptions import (
    InvalidCommentContent,
    InvalidPostException,
    InvalidUserException,
)
from fb_post.interactors.presenter_interfaces.create_comment_presenter_interface import (
    CreateCommentPresenterInterface,
)
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)


class CreateCommentInteractor:

    def __init__(self, post_storage: PostStorageInterface):
        self.post_storage = post_storage

    def create_comment_wrapper(
        self,
        user_id: int,
        post_id: int,
        comment_content: str,
        presenter: CreateCommentPresenterInterface,
    ):
        try:
            comment_id = self.create_comment(
                user_id=user_id,
                post_id=post_id,
                comment_content=comment_content,
            )
        except InvalidUserException:
            return presenter.raise_invalid_user_exception()
        except InvalidPostException:
            return presenter.raise_invalid_post_exception()
        except InvalidCommentContent:
            return presenter.raise_invalid_comment_content_exception()

        return presenter.get_create_comment_response(comment_id=comment_id)

    def create_comment(
        self,
        user_id: int,
        post_id: int,
        comment_content: str,
    ) -> int:
        """
        Validates and creates a comment on a post.

        Raises:
            InvalidUserException: when user does not exist
            InvalidPostException: when post does not exist
            InvalidCommentContent: when comment content is empty or whitespace
        """
        if not self.post_storage.does_user_exist(user_id=user_id):
            raise InvalidUserException

        if not self.post_storage.does_post_exist(post_id=post_id):
            raise InvalidPostException

        if not comment_content or not comment_content.strip():
            raise InvalidCommentContent

        return self.post_storage.create_comment(
            user_id=user_id,
            post_id=post_id,
            comment_content=comment_content,
        )