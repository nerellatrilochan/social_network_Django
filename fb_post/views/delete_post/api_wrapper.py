from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from fb_post.views.delete_post.validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.delete_post_interactor import DeletePostInteractor
    from fb_post.presenters.delete_post_presenter_implementation import (
        DeletePostPresenterImplementation,
    )
    from fb_post.storages.storage_implementation import StorageImplementation

    post_id = kwargs["path_params"]["post_id"]
    query_params = kwargs["query_params"]
    user_id = query_params["user_id"]

    post_storage = StorageImplementation()
    interactor = DeletePostInteractor(post_storage=post_storage)
    presenter = DeletePostPresenterImplementation()

    return interactor.delete_post_wrapper(
        user_id=user_id,
        post_id=post_id,
        presenter=presenter,
    )