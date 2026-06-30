from posts_auth.exceptions.custom_exceptions import \
    InvalidUserException, InvalidClientDetailsException, \
    GetUserProfileFailedException
from posts_auth.interactors.presenter_interfaces.\
    get_user_profile_presenter_interface import \
    GetUserProfilePresenterInterface


class GetUserProfileInteractor:

    def get_user_profile_wrapper(self, user_id: str,
                                 presenter: GetUserProfilePresenterInterface):
        try:
            user_profile_dto = self.get_user_profile(user_id=user_id)
        except InvalidUserException:
            return presenter.raise_invalid_user_exception()
        except InvalidClientDetailsException:
            return presenter.raise_invalid_client_details_exception()
        except GetUserProfileFailedException:
            return presenter.raise_get_user_profile_failed_exception()

        return presenter.prepare_response_for_get_user_profile(
            user_profile_dto=user_profile_dto)

    @staticmethod
    def get_user_profile(user_id: str):
        from posts_auth.adapters.service_adapter import \
            get_service_adapter
        adapter = get_service_adapter()
        user_profile_dto = adapter.auth_service.get_user_profile(user_id)
        return user_profile_dto
