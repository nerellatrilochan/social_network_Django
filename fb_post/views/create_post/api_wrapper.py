# fb_post/views/create_post/api_wrapper.py
from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.post_interactors import CreatePostInteractor
    from fb_post.presenters.json_presenter import JsonPresenter
    from fb_post.storages.storage_implementation import StorageImplementation

    request_data = kwargs["request_data"]

    return CreatePostInteractor().execute(
        user_id=request_data["user_id"],
        post_content=request_data["post_content"],
        storage=StorageImplementation(),
        presenter=JsonPresenter(),
    )