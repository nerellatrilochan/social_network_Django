from fb_post.constants.enum import ReactionTypeEnum
from fb_post.exceptions.custom_exceptions import (
    InvalidPostException,
    InvalidReactionTypeException,
    InvalidUserException,
)
from fb_post.interactors.presenter_interfaces.react_to_post_presenter_interface import (
    ReactToPostPresenterInterface,
)
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)


class ReactToPostInteractor:

    def __init__(self, post_storage: PostStorageInterface):
        self.post_storage = post_storage

    def react_to_post_wrapper(
        self,
        user_id: int,
        post_id: int,
        reaction_type: str,
        presenter: ReactToPostPresenterInterface,
    ):
        try:
            self.react_to_post(
                user_id=user_id,
                post_id=post_id,
                reaction_type=reaction_type,
            )
        except InvalidUserException:
            return presenter.raise_invalid_user_exception()
        except InvalidPostException:
            return presenter.raise_invalid_post_exception()
        except InvalidReactionTypeException:
            return presenter.raise_invalid_reaction_type_exception()

        return presenter.get_react_to_post_response()

    def react_to_post(
        self,
        user_id: int,
        post_id: int,
        reaction_type: str,
    ) -> None:
        """
        Validates and toggles a reaction on a post.

        - No existing reaction -> create one
        - Same reaction type already exists -> delete it (un-react)
        - Different reaction type -> update existing reaction

        Raises:
            InvalidUserException: when user does not exist
            InvalidPostException: when post does not exist
            InvalidReactionTypeException: when reaction type is invalid
        """
        if not self.post_storage.does_user_exist(user_id=user_id):
            raise InvalidUserException

        if not self.post_storage.does_post_exist(post_id=post_id):
            raise InvalidPostException

        valid_reaction_types = ReactionTypeEnum.get_list_of_values()
        if reaction_type not in valid_reaction_types:
            raise InvalidReactionTypeException

        self.post_storage.react_to_post(
            user_id=user_id,
            post_id=post_id,
            reaction_type=reaction_type,
        )