from posts_auth.adapters.service_adapter import get_service_adapter


class LogoutInteractor:

    def logout_wrapper(self, user_id: str):
        self.logout(user_id=user_id)

    @staticmethod
    def logout(user_id: str):
        service_adapter = get_service_adapter()
        service_adapter.auth_service. \
            logout_in_all_devices(user_id=user_id)
