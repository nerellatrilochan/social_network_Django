from django.db import models

from fb_post.constants.enum import ReactionTypeEnum
from fb_post.models.comment import Comment
from fb_post.models.post import Post
from fb_post.models.user import User


class Reaction(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reaction = models.CharField(
        max_length=100,
        choices=ReactionTypeEnum.get_list_of_tuples(),
    )
    reacted_at = models.DateTimeField(auto_now=True)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reacted_by", "post"],
                condition=models.Q(comment__isnull=True),
                name="unique_post_reaction_per_user",
            ),
        ]

    def __str__(self):
        return f"<Reaction: {self.id}>"