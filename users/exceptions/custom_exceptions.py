class NotRegisteredUser(Exception):
    pass


class InvalidAccessTokenException(Exception):
    pass


class RefreshTokenExpiredException(Exception):
    pass


class UserAccountDeactivatedException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UserAccountIsDeactivatedException(Exception):
    pass


class RefreshTokenNotFoundException(Exception):
    pass


class InvalidUserException(Exception):
    pass


class InvalidClientDetailsException(Exception):
    pass


class GetUserProfileFailedException(Exception):
    pass
