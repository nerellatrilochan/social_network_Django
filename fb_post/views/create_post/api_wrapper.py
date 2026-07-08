from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from fb_post.views.create_post.validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.create_post_interactor import CreatePostInteractor
    from fb_post.presenters.create_post_presenter_implementation import (
        CreatePostPresenterImplementation,
    )
    from fb_post.storages.storage_implementation import StorageImplementation

    request_data = kwargs["request_data"]

    post_storage = StorageImplementation()
    interactor = CreatePostInteractor(post_storage=post_storage)
    presenter = CreatePostPresenterImplementation()

    return interactor.create_post_wrapper(
        user_id=request_data["user_id"],
        post_content=request_data["post_content"],
        presenter=presenter,
    )