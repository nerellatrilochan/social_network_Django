from fb_post.exceptions.custom_exceptions import (
    InvalidPostException,
    InvalidUserException,
    UserCannotDeletePostException,
)
from fb_post.interactors.presenter_interfaces.delete_post_presenter_interface import (
    DeletePostPresenterInterface,
)
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)


class DeletePostInteractor:

    def __init__(self, post_storage: PostStorageInterface):
        self.post_storage = post_storage

    def delete_post_wrapper(
        self,
        user_id: int,
        post_id: int,
        presenter: DeletePostPresenterInterface,
    ):
        try:
            self.delete_post(user_id=user_id, post_id=post_id)
        except InvalidUserException:
            return presenter.raise_invalid_user_exception()
        except InvalidPostException:
            return presenter.raise_invalid_post_exception()
        except UserCannotDeletePostException:
            return presenter.raise_user_cannot_delete_post_exception()

        return presenter.get_delete_post_response()

    def delete_post(self, user_id: int, post_id: int) -> None:
        """
        Validates and deletes a post.

        Raises:
            InvalidUserException: when user does not exist
            InvalidPostException: when post does not exist
            UserCannotDeletePostException: when user is not the post owner
        """
        if not self.post_storage.does_user_exist(user_id=user_id):
            raise InvalidUserException

        posted_by_id = self.post_storage.get_post_owner_id(post_id=post_id)

        if posted_by_id != user_id:
            raise UserCannotDeletePostException

        self.post_storage.delete_post(post_id=post_id)