from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    refresh_token = request_data["refresh_token"]
    access_token = kwargs['access_token']

    from posts_auth.presenters.refresh_auth_tokens_presenter_imp import \
        RefreshAuthTokensPresenterImplementation
    from posts_auth.interactors.refresh_auth_tokens_interactor import \
        RefreshAuthTokensInteractor
    interactor = RefreshAuthTokensInteractor()
    presenter = RefreshAuthTokensPresenterImplementation()

    response = interactor.refresh_auth_tokens_wrapper(
        access_token=access_token,
        refresh_token=refresh_token,
        presenter=presenter
    )
    return response
