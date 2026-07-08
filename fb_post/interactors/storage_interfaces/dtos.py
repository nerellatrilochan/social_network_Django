from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class UserDetailsDTO:
    user_id: int
    name: str
    profile_pic: str


@dataclass
class ReactionsSummaryDTO:
    count: int
    type: List[str]


@dataclass
class CommentDetailsDTO:
    comment_id: int
    commenter: UserDetailsDTO
    commented_at: datetime
    comment_content: str
    reactions: ReactionsSummaryDTO
    replies_count: int
    replies: List["CommentDetailsDTO"]


@dataclass
class PostDetailsDTO:
    post_id: int
    posted_by: UserDetailsDTO
    posted_at: datetime
    post_content: str
    reactions: ReactionsSummaryDTO
    comments: List[CommentDetailsDTO]
    comments_count: int