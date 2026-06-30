import abc

from posts_auth.interactors.storage_interfaces.dtos import TokensDTO

class LoginPresenterInterface:

    @abc.abstractmethod
    def raise_invalid_credentials_exception(self):
        pass

    @abc.abstractmethod
    def raise_user_account_deactivated_exception(self):
        pass

    @abc.abstractmethod
    def get_response_for_login(self, token_dto: TokensDTO):
        pass
