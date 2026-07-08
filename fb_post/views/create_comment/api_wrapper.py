from dsu.dsu_gen.openapi.decorator.interface_decorator import validate_decorator

from fb_post.views.create_comment.validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from fb_post.interactors.create_comment_interactor import CreateCommentInteractor
    from fb_post.presenters.create_comment_presenter_implementation import (
        CreateCommentPresenterImplementation,
    )
    from fb_post.storages.storage_implementation import StorageImplementation

    request_data = kwargs["request_data"]

    post_storage = StorageImplementation()
    interactor = CreateCommentInteractor(post_storage=post_storage)
    presenter = CreateCommentPresenterImplementation()

    return interactor.create_comment_wrapper(
        user_id=request_data["user_id"],
        post_id=request_data["post_id"],
        comment_content=request_data["comment_content"],
        presenter=presenter,
    )