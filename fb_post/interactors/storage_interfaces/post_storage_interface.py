import abc


class PostStorageInterface:

    @abc.abstractmethod
    def does_user_exist(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    def create_post(self, user_id: int, post_content: str) -> int:
        pass