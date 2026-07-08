from datetime import datetime

from fb_post.constants.exception_messages import INVALID_POST
from fb_post.interactors.presenter_interfaces.get_post_presenter_interface import (
    GetPostPresenterInterface,
)
from fb_post.interactors.storage_interfaces.dtos import (
    CommentDetailsDTO,
    PostDetailsDTO,
    ReactionsSummaryDTO,
    UserDetailsDTO,
)
from social_network_mcp.presenters.mcp_response_mixin import McpResponseMixin


class McpGetPostPresenter(
    GetPostPresenterInterface,
    McpResponseMixin,
):

    def raise_invalid_post_exception(self) -> dict:
        return self.prepare_404_not_found_response({
            "response": INVALID_POST[0],
            "http_status_code": 404,
            "res_status": INVALID_POST[1],
        })

    def get_get_post_response(self, post_details_dto: PostDetailsDTO) -> dict:
        return self.prepare_200_success_response(
            self._convert_post_details_dto_to_dict(post_details_dto),
        )

    def _convert_post_details_dto_to_dict(
        self, post_details_dto: PostDetailsDTO,
    ) -> dict:
        return {
            "post_id": post_details_dto.post_id,
            "posted_by": self._convert_user_details_dto_to_dict(
                post_details_dto.posted_by,
            ),
            "posted_at": self._format_datetime(post_details_dto.posted_at),
            "post_content": post_details_dto.post_content,
            "reactions": self._convert_reactions_summary_dto_to_dict(
                post_details_dto.reactions,
            ),
            "comments": [
                self._convert_comment_details_dto_to_dict(comment)
                for comment in post_details_dto.comments
            ],
            "comments_count": post_details_dto.comments_count,
        }

    def _convert_comment_details_dto_to_dict(
        self, comment_details_dto: CommentDetailsDTO,
    ) -> dict:
        return {
            "comment_id": comment_details_dto.comment_id,
            "commenter": self._convert_user_details_dto_to_dict(
                comment_details_dto.commenter,
            ),
            "commented_at": self._format_datetime(
                comment_details_dto.commented_at,
            ),
            "comment_content": comment_details_dto.comment_content,
            "reactions": self._convert_reactions_summary_dto_to_dict(
                comment_details_dto.reactions,
            ),
            "replies_count": comment_details_dto.replies_count,
            "replies": [
                self._convert_comment_details_dto_to_dict(reply)
                for reply in comment_details_dto.replies
            ],
        }

    def _convert_user_details_dto_to_dict(
        self, user_details_dto: UserDetailsDTO,
    ) -> dict:
        return {
            "user_id": user_details_dto.user_id,
            "name": user_details_dto.name,
            "profile_pic": user_details_dto.profile_pic,
        }

    def _convert_reactions_summary_dto_to_dict(
        self, reactions_summary_dto: ReactionsSummaryDTO,
    ) -> dict:
        return {
            "count": reactions_summary_dto.count,
            "type": reactions_summary_dto.type,
        }

    @staticmethod
    def _format_datetime(datetime_obj: datetime) -> str:
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
