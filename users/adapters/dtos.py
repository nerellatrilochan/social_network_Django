from dataclasses import dataclass

from posts_auth.constants.enum import Gender, Language


@dataclass
class UserAuthTokensDTO:
    user_id: str
    access_token: str
    refresh_token: str
    expires_in: int


@dataclass
class UserProfileDTO:
    user_id: str
    name: str
    gender: Gender = None
    dob: str = None
    profile_pic_url: str = None
    phone_number: str = None
    country_code: str = None
    email: str = None
    language_preference: Language = None
    is_phone_number_verified: bool = None
    is_email_verified: bool = None
    cover_page_url: str = None
    age: int = None
    state_of_residence: str = None
    occupation: str = None
    i_want_to_receive_updates_directly_on_whatsapp: str = None
    last_name: str = None
    accepted_tnc: bool = False
    age_group: str = None
    pincode: str = None
