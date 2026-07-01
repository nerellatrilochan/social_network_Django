# fb_post/views/react_to_post/api_wrapper.py
from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.post_interactors import ReactToPostInteractor
    from fb_post.presenters.json_presenter import JsonPresenter
    from fb_post.storages.storage_implementation import StorageImplementation

    request_data = kwargs["request_data"]

    return ReactToPostInteractor().execute(
        user_id=request_data["user_id"],
        post_id=request_data["post_id"],
        reaction_type=request_data["reaction_type"],
        storage=StorageImplementation(),
        presenter=JsonPresenter(),
    )