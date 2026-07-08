import abc

from fb_post.interactors.storage_interfaces.dtos import PostDetailsDTO


class PostStorageInterface:

    @abc.abstractmethod
    def does_user_exist(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    def does_post_exist(self, post_id: int) -> bool:
        pass

    @abc.abstractmethod
    def create_post(self, user_id: int, post_content: str) -> int:
        pass

    @abc.abstractmethod
    def create_comment(
        self,
        user_id: int,
        post_id: int,
        comment_content: str,
    ) -> int:
        pass

    @abc.abstractmethod
    def react_to_post(
        self,
        user_id: int,
        post_id: int,
        reaction_type: str,
    ) -> None:
        pass

    @abc.abstractmethod
    def get_post_owner_id(self, post_id: int) -> int:
        pass

    @abc.abstractmethod
    def delete_post(self, post_id: int) -> None:
        pass

    @abc.abstractmethod
    def get_post_details(self, post_id: int) -> PostDetailsDTO:
        pass