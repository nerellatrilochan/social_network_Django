import abc

from django.http import HttpResponse

from posts_auth.adapters.dtos import UserProfileDTO


class GetUserProfilePresenterInterface:

    @abc.abstractmethod
    def raise_invalid_user_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_invalid_client_details_exception(self) -> HttpResponse:
        pass

    @abc.abstractmethod
    def prepare_response_for_get_user_profile(
            self, user_profile_dto: UserProfileDTO) -> HttpResponse:
        pass

    @abc.abstractmethod
    def raise_get_user_profile_failed_exception(self) -> HttpResponse:
        pass
