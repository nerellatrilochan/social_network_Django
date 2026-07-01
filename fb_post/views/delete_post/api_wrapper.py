# fb_post/views/delete_post/api_wrapper.py
from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.post_interactors import DeletePostInteractor
    from fb_post.presenters.json_presenter import JsonPresenter
    from fb_post.storages.storage_implementation import StorageImplementation

    post_id = kwargs["path_params"]["post_id"]
    request_data = kwargs.get("request_data") or {}
    query_params = kwargs.get("query_params") or {}
    user_id = request_data.get("user_id") or query_params["user_id"]

    return DeletePostInteractor().execute(
        user_id=user_id,
        post_id=post_id,
        storage=StorageImplementation(),
        presenter=JsonPresenter(),
    )