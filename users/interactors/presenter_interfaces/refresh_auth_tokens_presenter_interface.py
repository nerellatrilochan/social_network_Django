import abc

from posts_auth.adapters.dtos import UserAuthTokensDTO


class RefreshAuthTokensPresenterInterface:



    @abc.abstractmethod
    def raise_user_account_deactivated_exception(self):
        pass



    @abc.abstractmethod
    def raise_invalid_access_token_exception(self):
        pass

    @abc.abstractmethod
    def raise_refresh_token_expired_exception(self):
        pass

    @abc.abstractmethod
    def get_response_for_refresh_auth_tokens(self,
                                             auth_tokens_dto: UserAuthTokensDTO):
        pass

    @abc.abstractmethod
    def raise_refresh_token_not_found_exception(self):
        pass
