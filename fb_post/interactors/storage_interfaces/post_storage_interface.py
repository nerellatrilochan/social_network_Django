import abc

from fb_post.interactors.storage_interfaces.dtos import PostDetailsDTO


class PostStorageInterface:

    @abc.abstractmethod
    def does_user_exist(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    def create_post(self, user_id: int, post_content: str) -> int:
        pass

    @abc.abstractmethod
    def get_post_details(self, post_id: int) -> PostDetailsDTO:
        pass