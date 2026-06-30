from posts_auth.adapters.dtos import UserProfileDTO


class AuthService:

    @property
    def interface(self):
        from ib_users.interfaces.service_interface import ServiceInterface
        return ServiceInterface()

    @property
    def ib_account_helper_interface(self):
        from ib_user_accounts_helper.app_interfaces.service_interface import \
            ServiceInterface
        return ServiceInterface()

    def get_ib_accounts_access_token(self, code: str):
        from posts_auth.exceptions.custom_exceptions import \
            InvalidCredentialsException
        try:
            return self.ib_account_helper_interface.get_ib_accounts_access_token(
                code=code)
        except InvalidCredentialsException:
            raise InvalidCredentialsException

    def create_ib_accounts_auth_tokens(self, access_token: str,
                                       refresh_token: str, user_id: str, expires_in: int):
        return self.ib_account_helper_interface.create_ib_accounts_auth_tokens(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )

    def get_access_token(self, user_id: str):
        from posts_auth.exceptions.custom_exceptions import \
            UserAccountIsDeactivatedException

        try:
            return self.ib_account_helper_interface.get_access_token(
                user_id=user_id)
        except UserAccountIsDeactivatedException:
            raise UserAccountIsDeactivatedException

    def logout_in_all_devices(self, user_id: str):
        self.interface.logout_in_all_devices(user_id=user_id)

    def refresh_auth_tokens(self, access_token: str,
                            refresh_token: str):
        # pylint: disable=W0404
        from django_swagger_utils.drf_server.exceptions import NotFound
        from ib_users.validators.base_validator import CustomException

        try:
            auth_tokens_dto = self.interface.refresh_auth_tokens(
                access_token=access_token,
                refresh_token=refresh_token
            )
        except NotFound:
            from posts_auth.exceptions.custom_exceptions import \
                InvalidAccessTokenException
            raise InvalidAccessTokenException
        except CustomException as error:
            from posts_auth.constants.enum import ExceptionType
            if error.error_type == \
                    ExceptionType.USER_ACCOUNT_IS_DEACTIVATED.value:
                from posts_auth.exceptions.custom_exceptions import \
                    UserAccountDeactivatedException
                raise UserAccountDeactivatedException
            if error.error_type == \
                    ExceptionType.REFRESH_TOKEN_EXPIRED.value:
                from posts_auth.exceptions.custom_exceptions import \
                    RefreshTokenExpiredException
                raise RefreshTokenExpiredException
            if error.error_type == ExceptionType.REFRESH_TOKEN_NOT_FOUND.value:
                from posts_auth.exceptions.custom_exceptions import \
                    RefreshTokenNotFoundException
                raise RefreshTokenNotFoundException
            return

        from posts_auth.adapters.dtos import UserAuthTokensDTO
        return UserAuthTokensDTO(
            user_id=auth_tokens_dto.user_id,
            access_token=auth_tokens_dto.access_token,
            refresh_token=auth_tokens_dto.refresh_token,
            expires_in=auth_tokens_dto.expires_in
        )

    @staticmethod
    def create_user_in_ib_users(user_id):
        from ib_users.models import UserAccount
        try:
            UserAccount.objects.get(user_id=user_id)
        except UserAccount.DoesNotExist:
            UserAccount.objects.create(user_id=user_id)

    def get_user_profile(self, user_id):
        # pylint: disable=W0404
        from ib_user_accounts_helper.exceptions.custom_exceptions import \
            InvalidUserException, InvalidClientDetailsException, \
            GetUserProfileFailedException
        try:
            user_profile_dto = \
                self.ib_account_helper_interface.get_user_profile(user_id)
        except InvalidUserException:
            from posts_auth.exceptions.custom_exceptions import \
                InvalidUserException
            raise InvalidUserException
        except InvalidClientDetailsException:
            from posts_auth.exceptions.custom_exceptions import \
                InvalidClientDetailsException
            raise InvalidClientDetailsException
        except GetUserProfileFailedException:
            from posts_auth.exceptions.custom_exceptions import \
                GetUserProfileFailedException
            raise GetUserProfileFailedException

        return UserProfileDTO(
            name=user_profile_dto.name,
            user_id=user_profile_dto.user_id,
            gender=user_profile_dto.gender,
            dob=user_profile_dto.dob,
            profile_pic_url=user_profile_dto.profile_pic_url,
            phone_number=user_profile_dto.phone_number,
            country_code=user_profile_dto.country_code,
            email=user_profile_dto.email,
            language_preference=user_profile_dto.language_preference,
            is_phone_number_verified=user_profile_dto.is_phone_number_verified,
            is_email_verified=user_profile_dto.is_email_verified,
            cover_page_url=user_profile_dto.cover_page_url,
            age=user_profile_dto.age,
            state_of_residence=user_profile_dto.state_of_residence,
            occupation=user_profile_dto.occupation,
            i_want_to_receive_updates_directly_on_whatsapp=
            user_profile_dto.i_want_to_receive_updates_directly_on_whatsapp,
            last_name=user_profile_dto.last_name,
            accepted_tnc=user_profile_dto.accepted_tnc,
            pincode=user_profile_dto.pincode,
            age_group=user_profile_dto.age_group
        )
