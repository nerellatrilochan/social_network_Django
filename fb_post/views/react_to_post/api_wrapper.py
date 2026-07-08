from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from fb_post.views.react_to_post.validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.react_to_post_interactor import ReactToPostInteractor
    from fb_post.presenters.react_to_post_presenter_implementation import (
        ReactToPostPresenterImplementation,
    )
    from fb_post.storages.storage_implementation import StorageImplementation

    request_data = kwargs["request_data"]

    post_storage = StorageImplementation()
    interactor = ReactToPostInteractor(post_storage=post_storage)
    presenter = ReactToPostPresenterImplementation()

    return interactor.react_to_post_wrapper(
        user_id=request_data["user_id"],
        post_id=request_data["post_id"],
        reaction_type=request_data["reaction_type"],
        presenter=presenter,
    )