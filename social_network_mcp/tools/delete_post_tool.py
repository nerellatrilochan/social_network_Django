from typing import Any


def handle_delete_post(user_id: int, post_id: int) -> dict[str, Any]:
    from fb_post.interactors.delete_post_interactor import DeletePostInteractor
    from fb_post.storages.storage_implementation import StorageImplementation
    from social_network_mcp.presenters.mcp_delete_post_presenter import (
        McpDeletePostPresenter,
    )

    post_storage = StorageImplementation()
    interactor = DeletePostInteractor(post_storage=post_storage)
    presenter = McpDeletePostPresenter()

    return interactor.delete_post_wrapper(
        user_id=user_id,
        post_id=post_id,
        presenter=presenter,
    )
