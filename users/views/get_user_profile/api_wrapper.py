from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    from posts_auth.presenters. \
        get_user_profile_presenter_implementation import \
        GetUserProfilePresenterImplementation
    presenter = GetUserProfilePresenterImplementation()
    from posts_auth.interactors.get_user_profile_interactor import \
        GetUserProfileInteractor
    interactor = GetUserProfileInteractor()
    return interactor.get_user_profile_wrapper(user_id=str(user.user_id), presenter=presenter)
