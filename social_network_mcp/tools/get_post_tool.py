from typing import Any


def handle_get_post(post_id: int) -> dict[str, Any]:
    from fb_post.interactors.get_post_interactor import GetPostInteractor
    from fb_post.storages.storage_implementation import StorageImplementation
    from social_network_mcp.presenters.mcp_get_post_presenter import McpGetPostPresenter

    post_storage = StorageImplementation()
    interactor = GetPostInteractor(post_storage=post_storage)
    presenter = McpGetPostPresenter()

    return interactor.get_post_wrapper(
        post_id=post_id,
        presenter=presenter,
    )
