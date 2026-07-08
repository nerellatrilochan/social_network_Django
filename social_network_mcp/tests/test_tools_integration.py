import pytest
from fb_post.models.post import Post
from fb_post.models.user import User

from social_network_mcp.tools.create_comment_tool import handle_create_comment
from social_network_mcp.tools.create_post_tool import handle_create_post
from social_network_mcp.tools.delete_post_tool import handle_delete_post
from social_network_mcp.tools.get_post_tool import handle_get_post
from social_network_mcp.tools.react_to_post_tool import handle_react_to_post


@pytest.fixture
def user(db):
    return User.objects.create(name="Alice", profile_pic="pic.png")


@pytest.fixture
def post(user):
    result = handle_create_post(user_id=user.id, post_content="Hello MCP")
    return Post.objects.get(id=result["data"]["post_id"])


@pytest.mark.django_db
class TestMcpToolsIntegration:

    def test_create_post_success(self, user):
        result = handle_create_post(user_id=user.id, post_content="New post")

        assert result["ok"] is True
        assert result["status"] == 201
        assert "post_id" in result["data"]

    def test_create_post_invalid_user(self):
        result = handle_create_post(user_id=9999, post_content="New post")

        assert result["ok"] is False
        assert result["status"] == 400
        assert result["error"]["res_status"] == "INVALID_USER_EXCEPTION"

    def test_get_post_success(self, post):
        result = handle_get_post(post_id=post.id)

        assert result["ok"] is True
        assert result["status"] == 200
        assert result["data"]["post_id"] == post.id
        assert result["data"]["post_content"] == "Hello MCP"

    def test_get_post_not_found(self):
        result = handle_get_post(post_id=9999)

        assert result["ok"] is False
        assert result["status"] == 404

    def test_create_comment_success(self, user, post):
        result = handle_create_comment(
            user_id=user.id,
            post_id=post.id,
            comment_content="Nice post",
        )

        assert result["ok"] is True
        assert result["status"] == 201
        assert "comment_id" in result["data"]

    def test_react_to_post_success(self, user, post):
        result = handle_react_to_post(
            user_id=user.id,
            post_id=post.id,
            reaction_type="LOVE",
        )

        assert result["ok"] is True
        assert result["status"] == 200

    def test_react_to_post_invalid_reaction(self, user, post):
        result = handle_react_to_post(
            user_id=user.id,
            post_id=post.id,
            reaction_type="INVALID",
        )

        assert result["ok"] is False
        assert result["status"] == 400
        assert result["error"]["res_status"] == "INVALID_REACTION_TYPE_EXCEPTION"

    def test_delete_post_success(self, user, post):
        result = handle_delete_post(user_id=user.id, post_id=post.id)

        assert result["ok"] is True
        assert result["status"] == 200
        assert not Post.objects.filter(id=post.id).exists()

    def test_delete_post_forbidden(self, user, post):
        other_user = User.objects.create(name="Bob", profile_pic="pic2.png")
        result = handle_delete_post(user_id=other_user.id, post_id=post.id)

        assert result["ok"] is False
        assert result["status"] == 403
        assert result["error"]["res_status"] == "USER_CANNOT_DELETE_POST_EXCEPTION"
