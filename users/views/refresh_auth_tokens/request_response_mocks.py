

REQUEST_BODY_JSON = """
{
    "refresh_token": "string"
}
"""


RESPONSE_200_JSON = """
{
    "access_token": "string",
    "user_id": "string",
    "refresh_token": "string",
    "expires_in": 1
}
"""

RESPONSE_400_JSON = """
{
    "response": "string",
    "http_status_code": 1,
    "res_status": "INVALID_ACCESS_TOKEN"
}
"""

RESPONSE_403_JSON = """
{
    "response": "string",
    "http_status_code": 1,
    "res_status": "USER_ACCOUNT_IS_DEACTIVATED"
}
"""

RESPONSE_404_JSON = """
{
    "response": "string",
    "http_status_code": 1,
    "res_status": "REFRESH_TOKEN_NOT_FOUND"
}
"""

