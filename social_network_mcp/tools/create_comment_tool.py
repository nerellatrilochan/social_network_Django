from typing import Any


def handle_create_comment(
    user_id: int,
    post_id: int,
    comment_content: str,
) -> dict[str, Any]:
    from fb_post.interactors.create_comment_interactor import CreateCommentInteractor
    from fb_post.storages.storage_implementation import StorageImplementation
    from social_network_mcp.presenters.mcp_create_comment_presenter import (
        McpCreateCommentPresenter,
    )

    post_storage = StorageImplementation()
    interactor = CreateCommentInteractor(post_storage=post_storage)
    presenter = McpCreateCommentPresenter()

    return interactor.create_comment_wrapper(
        user_id=user_id,
        post_id=post_id,
        comment_content=comment_content,
        presenter=presenter,
    )
