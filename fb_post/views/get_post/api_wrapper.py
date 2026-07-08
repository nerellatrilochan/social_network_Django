from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from fb_post.views.get_post.validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.get_post_interactor import GetPostInteractor
    from fb_post.presenters.get_post_presenter_implementation import (
        GetPostPresenterImplementation,
    )
    from fb_post.storages.storage_implementation import StorageImplementation

    post_id = kwargs["path_params"]["post_id"]

    post_storage = StorageImplementation()
    interactor = GetPostInteractor(post_storage=post_storage)
    presenter = GetPostPresenterImplementation()

    return interactor.get_post_wrapper(
        post_id=post_id,
        presenter=presenter,
    )