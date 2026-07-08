from fb_post.exceptions.custom_exceptions import (
    InvalidPostException,
    InvalidUserException,
    UserCannotDeletePostException,
)


class DeletePostInteractor:
    def execute(self, user_id, post_id, storage, presenter):
        try:
            storage.validate_user(user_id)
            storage.validate_post(post_id)
            storage.validate_user_can_delete_post(user_id, post_id)
            storage.delete_post(post_id)
        except InvalidUserException:
            return presenter.raise_exception_for_invalid_user()
        except InvalidPostException:
            return presenter.raise_exception_for_invalid_post_bad_request()
        except UserCannotDeletePostException:
            return presenter.raise_exception_for_user_cannot_delete_post()

        return presenter.prepare_200_success_response({})