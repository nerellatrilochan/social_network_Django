import json

import pytest
from django.http import response

from posts_auth.presenters.get_user_profile_presenter_implementation import \
    INVALID_USER_ID, INVALID_CLIENT_CREDENTIALS


class TestGetUserProfilePresenterImplementation:

    @pytest.fixture
    def presenter(self):
        from posts_auth.presenters.\
            get_user_profile_presenter_implementation import \
            GetUserProfilePresenterImplementation
        return GetUserProfilePresenterImplementation()

    def test_raise_invalid_credentials_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": INVALID_CLIENT_CREDENTIALS[0],
            "http_status_code": 400,
            "res_status": INVALID_CLIENT_CREDENTIALS[1]
        })
        expected_http_response = response.HttpResponse(data, status=400)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_invalid_client_details_exception()

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response

    def test_raise_invalid_user_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": INVALID_USER_ID[0],
            "http_status_code": 400,
            "res_status": INVALID_USER_ID[1]
        })
        expected_http_response = response.HttpResponse(data, status=400)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_invalid_user_exception()

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response

    def test_prepare_response_for_get_user_profile(self, presenter):
        # Arrange
        user_profile_dict = {
            "user_id": "user_1",
            "phone_number": "98765431",
            "country_code": "91",
            "email": "my_email_1",
            "profile_pic_url": "my_profile_1",
            "name": "name_1",
            "dob": "2020-12-28",
            "gender": "MALE",
            "cover_page_url": "name_1",
            "age": 20,
            "state_of_residence": "my_profile_1",
            "occupation": "occupation_1",
            "is_email_verified": False,
            "is_phone_number_verified": False,
            "i_want_to_receive_updates_directly_on_whatsapp": "yes",
            "last_name": "last_name_1",
            "accepted_tnc": True,
            "pincode": "534313",
            "age_group": "age_group1",
            "language_preference": "ENGLISH"
        }
        from posts_auth.tests.factories.adapter_dtos import \
            UserProfileDTOFactory
        UserProfileDTOFactory.reset_sequence()
        user_profile_dto = UserProfileDTOFactory.create_batch(1)[0]
        data = json.dumps(user_profile_dict)
        expected_http_response = response.HttpResponse(data, status=200)
        expected_response = json.loads(expected_http_response.content)

        # Act
        actual_http_response = presenter.prepare_response_for_get_user_profile(
            user_profile_dto=user_profile_dto
        )
        # Assert
        actual_response = json.loads(actual_http_response.content)
        assert actual_response == expected_response
