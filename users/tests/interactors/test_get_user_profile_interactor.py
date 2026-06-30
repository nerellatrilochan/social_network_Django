from unittest.mock import create_autospec, Mock

import pytest


class TestGetUserProfilesBulkInteractor:

    @pytest.fixture
    def presenter_mock(self):
        from posts_auth.interactors.presenter_interfaces. \
            get_user_profile_presenter_interface import \
            GetUserProfilePresenterInterface
        presenter = create_autospec(GetUserProfilePresenterInterface)
        return presenter

    @pytest.fixture
    def interactor(self):
        from posts_auth.interactors.get_user_profile_interactor import \
            GetUserProfileInteractor
        interactor = GetUserProfileInteractor()
        return interactor

    def test_given_invalid_client_then_raise_exception(
            self, presenter_mock, interactor, mocker):
        # Arrange
        user_id = '16fd2706-8baf-433b-82eb-8c7fada847da'
        expected_response = Mock()

        from posts_auth.tests.common_fixtures.adapters import \
            get_user_profile_mock
        from posts_auth.exceptions.custom_exceptions import \
            InvalidClientDetailsException
        get_user_profile_mock = get_user_profile_mock(mocker)
        get_user_profile_mock.side_effect = \
            InvalidClientDetailsException()

        presenter_mock.raise_invalid_client_details_exception.return_value = \
            expected_response

        # Act
        actual_response = interactor.get_user_profile_wrapper(
            user_id=user_id,
            presenter=presenter_mock
        )

        # Assert
        assert actual_response == expected_response
        presenter_mock.raise_invalid_client_details_exception.\
            assert_called_once()
        get_user_profile_mock.assert_called_once_with(user_id)

    def test_given_invalid_user_then_raise_exception(
            self, presenter_mock, interactor, mocker):
        # Arrange
        user_id = '16fd2706-8baf-433b-82eb-8c7fada847da'
        expected_response = Mock()

        from posts_auth.tests.common_fixtures.adapters import \
            get_user_profile_mock
        from posts_auth.exceptions.custom_exceptions import \
            InvalidUserException
        get_user_profile_mock = get_user_profile_mock(mocker)
        get_user_profile_mock.side_effect = \
            InvalidUserException()

        presenter_mock.raise_invalid_user_exception.return_value = \
            expected_response

        # Act
        actual_response = interactor.get_user_profile_wrapper(
            user_id=user_id,
            presenter=presenter_mock
        )

        # Assert
        assert actual_response == expected_response
        presenter_mock.raise_invalid_user_exception.assert_called_once()
        get_user_profile_mock.assert_called_once_with(user_id)

    def test_given_valid_details_return_user_profile(
            self, presenter_mock, interactor, mocker):
        # Arrange
        user_id = '16fd2706-8baf-433b-82eb-8c7fada847da'
        expected_response = Mock()

        from posts_auth.tests.common_fixtures.adapters import \
            get_user_profile_mock
        from posts_auth.tests.factories.adapter_dtos import \
            UserProfileDTOFactory
        UserProfileDTOFactory.reset_sequence()
        user_profile_dto = UserProfileDTOFactory.create_batch(1)[0]
        get_user_profile_mock = get_user_profile_mock(mocker)
        get_user_profile_mock.return_value = user_profile_dto

        presenter_mock.prepare_response_for_get_user_profile.return_value = \
            expected_response

        # Act
        actual_response = interactor.get_user_profile_wrapper(
            user_id=user_id,
            presenter=presenter_mock
        )

        # Assert
        assert actual_response == expected_response
        presenter_mock.prepare_response_for_get_user_profile.\
            assert_called_once_with(user_profile_dto=user_profile_dto)
        get_user_profile_mock.assert_called_once_with(user_id)
