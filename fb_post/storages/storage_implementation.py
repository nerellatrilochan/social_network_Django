from collections import defaultdict

from django.db.models import Prefetch

from fb_post.constants.enum import ReactionTypeEnum
from fb_post.exceptions.custom_exceptions import (
    InvalidCommentContent,
    InvalidPostContent,
    InvalidPostException,
    InvalidReactionTypeException,
    InvalidUserException,
    UserCannotDeletePostException,
)
from fb_post.interactors.storage_interfaces.dtos import (
    CommentDetailsDTO,
    PostDetailsDTO,
    ReactionsSummaryDTO,
    UserDetailsDTO,
)
from fb_post.interactors.storage_interfaces.post_storage_interface import (
    PostStorageInterface,
)
from fb_post.models import Comment, Post, Reaction, User


class StorageImplementation(PostStorageInterface):

    def does_user_exist(self, user_id: int) -> bool:
        return User.objects.filter(id=user_id).exists()

    def does_post_exist(self, post_id: int) -> bool:
        return Post.objects.filter(id=post_id).exists()

    def validate_user(self, user_id):
        if not User.objects.filter(id=user_id).exists():
            raise InvalidUserException

    def validate_post(self, post_id):
        if not Post.objects.filter(id=post_id).exists():
            raise InvalidPostException

    def validate_post_content(self, content):
        if not content or not content.strip():
            raise InvalidPostContent

    def validate_comment_content(self, content):
        if not content or not content.strip():
            raise InvalidCommentContent

    def validate_reaction_type(self, reaction_type):
        valid_reactions = [reaction.value for reaction in ReactionTypeEnum]
        if reaction_type not in valid_reactions:
            raise InvalidReactionTypeException

    def create_post(self, user_id: int, post_content: str) -> int:
        post = Post.objects.create(posted_by_id=user_id, content=post_content)
        return post.id

    def create_comment(
        self,
        user_id: int,
        post_id: int,
        comment_content: str,
    ) -> int:
        comment = Comment.objects.create(
            commented_by_id=user_id,
            post_id=post_id,
            content=comment_content,
        )
        return comment.id

    def react_to_post(self, user_id, post_id, reaction_type):
        reaction = Reaction.objects.filter(
            reacted_by_id=user_id,
            post_id=post_id,
            comment__isnull=True,
        ).first()

        if reaction is None:
            Reaction.objects.create(
                reacted_by_id=user_id,
                post_id=post_id,
                reaction=reaction_type,
            )
            return

        if reaction.reaction == reaction_type:
            reaction.delete()
            return

        reaction.reaction = reaction_type
        reaction.save(update_fields=["reaction", "reacted_at"])

    def validate_user_can_delete_post(self, user_id, post_id):
        post = Post.objects.get(id=post_id)
        if post.posted_by_id != int(user_id):
            raise UserCannotDeletePostException

    def delete_post(self, post_id):
        Post.objects.get(id=post_id).delete()

    def get_post_details(self, post_id: int) -> PostDetailsDTO:
        comments_queryset = (
            Comment.objects.select_related("commented_by", "parent_comment")
            .prefetch_related("reaction_set")
            .order_by("commented_at")
        )

        try:
            post = (
                Post.objects.select_related("posted_by")
                .prefetch_related(
                    "reaction_set",
                    Prefetch("comment_set", queryset=comments_queryset),
                )
                .get(id=post_id)
            )
        except Post.DoesNotExist:
            raise InvalidPostException

        comments = list(post.comment_set.all())
        children_by_parent_id = defaultdict(list)
        for comment in comments:
            children_by_parent_id[comment.parent_comment_id].append(comment)

        top_level_comments = children_by_parent_id[None]

        return PostDetailsDTO(
            post_id=post.id,
            posted_by=self._to_user_details_dto(post.posted_by),
            posted_at=post.posted_at,
            post_content=post.content,
            reactions=self._to_reactions_summary_dto(post.reaction_set.all()),
            comments=[
                self._to_comment_details_dto(comment, children_by_parent_id)
                for comment in top_level_comments
            ],
            comments_count=len(comments),
        )

    @staticmethod
    def _to_user_details_dto(user) -> UserDetailsDTO:
        return UserDetailsDTO(
            user_id=user.id,
            name=user.name,
            profile_pic=user.profile_pic,
        )

    @staticmethod
    def _to_reactions_summary_dto(reactions) -> ReactionsSummaryDTO:
        reaction_list = list(reactions)
        return ReactionsSummaryDTO(
            count=len(reaction_list),
            type=sorted({reaction.reaction for reaction in reaction_list}),
        )

    def _to_comment_details_dto(
        self, comment, children_by_parent_id,
    ) -> CommentDetailsDTO:
        replies = children_by_parent_id[comment.id]
        return CommentDetailsDTO(
            comment_id=comment.id,
            commenter=self._to_user_details_dto(comment.commented_by),
            commented_at=comment.commented_at,
            comment_content=comment.content,
            reactions=self._to_reactions_summary_dto(comment.reaction_set.all()),
            replies_count=len(replies),
            replies=[
                self._to_comment_details_dto(reply, children_by_parent_id)
                for reply in replies
            ],
        )