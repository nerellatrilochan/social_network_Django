from unittest.mock import patch

from posts_auth.interactors.logout_interactor import LogoutInteractor


class TestLogoutInteractor:

    @patch(
        "users.adapters.user_service.AuthService.logout_in_all_devices"
    )
    def test_log_out_interactor(self, logout_in_all_devices):
        # Arrange
        interactor = LogoutInteractor()
        user_id = "2a6de048-5cf7-4ae1-8555-51e1c59984fb"

        # Act
        interactor.logout_wrapper(user_id=user_id)

        # Assert
        logout_in_all_devices.assert_called_once_with(user_id=user_id)
