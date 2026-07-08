from typing import Any


def handle_react_to_post(
    user_id: int,
    post_id: int,
    reaction_type: str,
) -> dict[str, Any]:
    from fb_post.interactors.react_to_post_interactor import ReactToPostInteractor
    from fb_post.storages.storage_implementation import StorageImplementation
    from social_network_mcp.presenters.mcp_react_to_post_presenter import (
        McpReactToPostPresenter,
    )

    post_storage = StorageImplementation()
    interactor = ReactToPostInteractor(post_storage=post_storage)
    presenter = McpReactToPostPresenter()

    return interactor.react_to_post_wrapper(
        user_id=user_id,
        post_id=post_id,
        reaction_type=reaction_type,
        presenter=presenter,
    )
