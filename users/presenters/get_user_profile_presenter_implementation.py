from django.http import response, HttpResponse

from posts_auth.adapters.dtos import UserProfileDTO
from posts_auth.interactors.presenter_interfaces.\
    get_user_profile_presenter_interface import \
    GetUserProfilePresenterInterface


INVALID_USER_ID = (
    "Given Invalid User id",
    "INVALID_USER_ID"
)

INVALID_CLIENT_CREDENTIALS = (
    "Invalid Client Credentials",
    "INVALID_CLIENT_CREDENTIALS"
)

GET_USER_PROFILE_FAILED = (
    'Get User profile failed',
    'GET_USER_PROFILE_FAILED'
)


class GetUserProfilePresenterImplementation(GetUserProfilePresenterInterface):

    def raise_invalid_user_exception(self) -> HttpResponse:
        import json
        data = json.dumps({
            "response": INVALID_USER_ID[0],
            "http_status_code": 400,
            "res_status": INVALID_USER_ID[1]
        })

        response_object = response.HttpResponse(data, status=400)
        return response_object

    def raise_invalid_client_details_exception(self) -> HttpResponse:
        import json
        data = json.dumps({
            "response": INVALID_CLIENT_CREDENTIALS[0],
            "http_status_code": 400,
            "res_status": INVALID_CLIENT_CREDENTIALS[1]
        })

        response_object = response.HttpResponse(data, status=400)
        return response_object

    def prepare_response_for_get_user_profile(
            self, user_profile_dto: UserProfileDTO) -> HttpResponse:
        import json
        data = json.dumps({
            "user_id": user_profile_dto.user_id,
            "phone_number": user_profile_dto.phone_number,
            "country_code": user_profile_dto.country_code,
            "email": user_profile_dto.email,
            "profile_pic_url": user_profile_dto.profile_pic_url,
            "name": user_profile_dto.name,
            "dob": str(user_profile_dto.dob),
            "gender": user_profile_dto.gender,
            "cover_page_url": user_profile_dto.cover_page_url,
            "age": user_profile_dto.age,
            "state_of_residence": user_profile_dto.state_of_residence,
            "occupation": user_profile_dto.occupation,
            "is_email_verified": user_profile_dto.is_email_verified,
            "is_phone_number_verified": user_profile_dto.is_phone_number_verified,
            "i_want_to_receive_updates_directly_on_whatsapp": user_profile_dto.\
                i_want_to_receive_updates_directly_on_whatsapp,
            "last_name": user_profile_dto.last_name,
            "accepted_tnc": user_profile_dto.accepted_tnc,
            "pincode": user_profile_dto.pincode,
            "age_group": user_profile_dto.age_group,
            "language_preference": user_profile_dto.language_preference
        })
        response_object = response.HttpResponse(data, status=200)
        return response_object

    def raise_get_user_profile_failed_exception(self) -> HttpResponse:
        import json
        data = json.dumps({
            "response": GET_USER_PROFILE_FAILED[0],
            "http_status_code": 400,
            "res_status": GET_USER_PROFILE_FAILED[1]
        })

        response_object = response.HttpResponse(data, status=400)
        return response_object
