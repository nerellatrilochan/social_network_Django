from django.db import models

from fb_post.models.post import Post
from fb_post.models.user import User


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"<Comment: {self.id}>"