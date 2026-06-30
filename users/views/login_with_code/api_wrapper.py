from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from posts_auth.interactors.login_interactor import \
        LoginInteractor
    interactor = LoginInteractor()

    from posts_auth.presenters.login_presenter_imp import \
        LoginPresenterImplementation
    presenter = LoginPresenterImplementation()

    request_data = kwargs['request_data']
    client_id = request_data['client_id']
    code = request_data['code']

    response = interactor.login_wrapper(client_id=client_id,
                                        code=code,
                                        presenter=presenter)
    return response
