from typing import Any


def handle_create_post(user_id: int, post_content: str) -> dict[str, Any]:
    from fb_post.interactors.create_post_interactor import CreatePostInteractor
    from fb_post.storages.storage_implementation import StorageImplementation
    from social_network_mcp.presenters.mcp_create_post_presenter import (
        McpCreatePostPresenter,
    )

    post_storage = StorageImplementation()
    interactor = CreatePostInteractor(post_storage=post_storage)
    presenter = McpCreatePostPresenter()

    return interactor.create_post_wrapper(
        user_id=user_id,
        post_content=post_content,
        presenter=presenter,
    )
