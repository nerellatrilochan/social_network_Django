# ruff: noqa: S105

from enum import Enum

from ib_common.constants import BaseEnumClass


class ExceptionType(BaseEnumClass, Enum):
    REFRESH_TOKEN_NOT_FOUND = 'REFRESH_TOKEN_NOT_FOUND'
    REFRESH_TOKEN_EXPIRED = 'REFRESH_TOKEN_EXPIRED'
    USER_ACCOUNT_IS_DEACTIVATED = 'USER_ACCOUNT_IS_DEACTIVATED'


class Gender(BaseEnumClass, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Language(BaseEnumClass, Enum):
    ENGLISH = "ENGLISH"
    TELUGU = "TELUGU"
