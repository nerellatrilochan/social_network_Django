from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from posts_auth.interactors.logout_interactor import LogoutInteractor
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    user_id = user.user_id
    interactor = LogoutInteractor()
    response = interactor.logout_wrapper(user_id=user_id)
    return response
