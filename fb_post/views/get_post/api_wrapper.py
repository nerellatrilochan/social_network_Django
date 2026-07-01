# fb_post/views/get_post/api_wrapper.py
from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.post_interactors import GetPostInteractor
    from fb_post.presenters.json_presenter import JsonPresenter
    from fb_post.storages.storage_implementation import StorageImplementation

    post_id = kwargs["path_params"]["post_id"]

    return GetPostInteractor().execute(
        post_id=post_id,
        storage=StorageImplementation(),
        presenter=JsonPresenter(),
    )