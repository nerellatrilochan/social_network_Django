## Tasks
1. Scaffold & register the DSU app
2. Write the Social Network models
3. Write the OpenAPI spec
4. Build the views
5. Implement create_post (api_wrapper + interactor + storage + presenter)
6. Implement get_post
7. Implement create_comment
8. Implement react_to_post
9. Implement delete_post
10. Domain Overview

You are building a subset of the Social Network application from Assignment 006. The full data model is described there — here you will expose five of its operations as REST APIs through DSU.

## The five endpoints you will implement:

| Operation        | HTTP Method + Path	                        | Key behaviour                                   |
| `create_post`    | `POST` `/fb_post/create_post/v1/`	        | Returns `post_id`. Raises 400 for invalid user or empty content  |
| `get_post`	   | `GET`  `/fb_post/get_post/v1/{post_id}/`   | Returns full post details with comments & reactions. Raises 404 for unknown post.  |
| `create_comment` | `POST`  `/fb_post/create_comment/v1/`	   | Returns `comment_id`. Raises 400 for invalid user, post, or empty content. |
| `react_to_post`  | `POST`  `/fb_post/react_to_post/v1/`	   | Toggle-react logic. Raises 400 for invalid user, post, or reaction type. | 
| `delete_post`	| `DELETE` `/fb_post/delete_post/v1/{post_id}/` | 	Cascades delete. Raises 403 if user is not the post creator. |

Reminder — full Clean Architecture flow in DSU:
Every request travels: urls.py → view file → validator_class → api_wrapper → interactor → storage / presenter
urls.py → view file(auto-gen) → validator_class → api_wrapper(you write) → interactor → storage presenter

# Phase 1 — Setup

## Task 1 - Scaffold & Register the DSU App
Create the DSU project and app from scratch using the DSU management commands.

- Run `python manage.py create_cleanapp fb_post -p social_network` to scaffold the app with a full Clean Architecture folder structure.
- Open `settings/base_swagger_utils.py` and register the app in both required places:
```
# 1. In the INSTALLED_APPS / APPS list:
"fb_post",

# 2. In SWAGGER_UTILS["APPS"]:
"fb_post": {
    "prefix_url": "fb_post",
},
```
- Start the server and confirm Django starts without errors.
Common mistake: Forgetting the second registration in `SWAGGER_UTILS["APPS"]`. If your endpoints don't appear after `build`, this is the first thing to check.

## Task 2 - Write the Social Network Models
In `fb_post/models/` (or a single `models.py`), define the following models exactly as described in Assignment 006 — Task 1. Use the exact field and class names from the spec.

- User — `name` (CharField, max 100), `profile_pic`(TextField)
- Post — `content` (max 1000), `posted_at` (DateTimeField, auto_now_add), `posted_by` (FK → User)
- Comment — `content` (max 1000), `commented_at` (auto_now_add), `commented_by` (FK → User), `post` (FK → Post), `parent_comment` (nullable FK → self)
- Reaction — `post` (nullable FK → Post), `comment` (nullable FK → Comment), `reaction` (CharField, max 100), `reacted_at`(auto_now), `reacted_by` (FK → User)
- Write the reaction type choices as an enum in `fb_post/constants.py` : `WOW, LIT, LOVE, HAHA, THUMBS-UP, THUMBS-DOWN, ANGRY, SAD`
Write the custom exceptions in `fb_post/exceptions.py` :
`InvalidUserException, InvalidPostException, InvalidPostContent, InvalidCommentContent, InvalidReactionTypeException, UserCannotDeletePostException`
Run `python manage.py makemigrations fb_post && python manage.py migrate` — confirm no errors.


# Phase 2 - OpenAPI Spec + Build

## Task 3 - Write the OpenAPI Spec
- Create `fb_post/api_specs/api_spec.json`. This file drives everything DSU generates — every `operationId` becomes a view folder.
- You need to define all five endpoints. The scaffolds below show the structure — fill in the request/response schemas yourself.
- DSU operationId naming convention: Use snake_case. DSU generates a folder `fb_post/views/<operationId>/` for each one.

POST `/fb_post/create_post/v1/` 

Request Body
{
  "user_id": 1,
  "post_content": "Hello world!"
}

201 Response
{ "post_id": 42 }

400 Response (invalid user / empty content)
{
  "response": "Invalid user",
  "http_status_code": 400,
  "res_status": "INVALID_USER_EXCEPTION"
}

GET `/fb_post/get_post/v1/{post_id}/`

200 Response
{
  "post_id": 1,
  "posted_by": { "name": "Alice", "user_id": 1, "profile_pic": "..." },
  "posted_at": "2024-01-01 10:00:00",
  "post_content": "Hello world!",
  "reactions": { "count": 3, "type": ["WOW", "LOVE"] },
  "comments": [
    {
      "comment_id": 1,
      "commenter": { "user_id": 2, "name": "Bob", "profile_pic": "..." },
      "commented_at": "2024-01-01 10:05:00",
      "comment_content": "Great post!",
      "reactions": { "count": 1, "type": ["THUMBS-UP"] },
      "replies_count": 0,
      "replies": []
    }
  ],
  "comments_count": 1
}

404 Response (post not found)
{
  "response": "Post not found",
  "http_status_code": 404,
  "res_status": "INVALID_POST_EXCEPTION"
}

POST `/fb_post/create_comment/v1/`

Request Body
{
  "user_id": 1,
  "post_id": 42,
  "comment_content": "Nice post!"
}

201 Response
{ "comment_id": 7 }

POST `/fb_post/react_to_post/v1/`

Request Body
{
  "user_id": 1,
  "post_id": 42,
  "reaction_type": "WOW"
}

200 Response (no body needed)
{}

DELETE `/fb_post/delete_post/v1/{post_id}/`

The user_id of the requester should come from `kwargs['request_data']` or a query param — your choice. Respond 200 on success, 400 if user is not the creator.

 - All five paths defined in `api_spec.json` with correct `operationId` values.
 - All request/response schemas are JSON Schema objects (type, properties, required).
 - Error responses always contain `response`, `http_status_code`, `res_status`.

## Task 4 - Build the Views
Run the DSU build command for your app: `python manage.py build -a fb_post`

 - Verify that five folders are created under `fb_post/views/`, one per `operationId`.
 - Each folder should contain: `api_wrapper.py`, `<operation_id>.py`, `request_response_mocks.py`, `validator_class.py`,
   `__init__.py`.
 - Open each `__init__.py` and confirm it says `ENV_MOCK`(the default). Do not switch to `ENV_IMPL` yet.
 - Start the server and hit any of the five endpoints — DSU should return mock data (status 200 with stub values). This       confirms the spec + build pipeline is working.
 Tip: Use Swagger UI at `/swagger/` (or `/api/schema/swagger-ui/`) to browse and test your endpoints without writing any curl commands.


 

