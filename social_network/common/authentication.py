import logging

from rest_framework.authentication import (BaseAuthentication)
from rest_framework_api_key.permissions import HasAPIKey

logger = logging.getLogger(__name__)


class APIKeyAuthentication(BaseAuthentication, HasAPIKey):
    """Token based authentication using the JSON Web Token standard."""

    def __init__(self):
        super(APIKeyAuthentication, self).__init__()

    def authenticate(self, request):
        from rest_framework.exceptions import NotAuthenticated
        has_permission = self.has_permission(request, None)

        if not has_permission:
            raise NotAuthenticated()

        return None, None
