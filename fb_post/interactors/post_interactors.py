from fb_post.exceptions.custom_exceptions import (
    InvalidPostException,
    InvalidReactionTypeException,
    InvalidUserException,
    UserCannotDeletePostException,
)


class ReactToPostInteractor:
    def execute(self, user_id, post_id, reaction_type, storage, presenter):
        try:
            storage.validate_user(user_id)
            storage.validate_post(post_id)
            storage.validate_reaction_type(reaction_type)
            storage.react_to_post(user_id, post_id, reaction_type)
        except InvalidUserException:
            return presenter.raise_exception_for_invalid_user()
        except InvalidPostException:
            return presenter.raise_exception_for_invalid_post_bad_request()
        except InvalidReactionTypeException:
            return presenter.raise_exception_for_invalid_reaction_type()

        return presenter.prepare_200_success_response({})


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