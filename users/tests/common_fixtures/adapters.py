
def refresh_auth_tokens_mock(mocker):
    return mocker.patch("users.adapters.user_service.AuthService"
                        ".refresh_auth_tokens")

def get_ib_accounts_access_token(mocker):
    return mocker.patch('users.adapters.user_service.AuthService'
                        '.get_ib_accounts_access_token')

def create_ib_accounts_auth_tokens(mocker):
    return mocker.patch('users.adapters.user_service.AuthService'
                        '.create_ib_accounts_auth_tokens')

def create_user_in_ib_users(mocker):
    return mocker.patch('users.adapters.user_service.AuthService'
                        '.create_user_in_ib_users')

def get_access_token(mocker):
    return mocker.patch('users.adapters.user_service.AuthService'
                        '.get_access_token')

def logout_in_all_devices(mocker):
    return mocker.patch("users.adapters.user_service.AuthService"
                        ".logout_in_all_devices")


def get_user_profile_mock(mocker):
    return mocker.patch("users.adapters.user_service.AuthService"
                        ".get_user_profile")
