

REQUEST_BODY_JSON = """
{
    "client_id": "string",
    "code": "string"
}
"""


RESPONSE_200_JSON = """
{
    "access_token": "string",
    "refresh_token": "string",
    "expires_in": 1
}
"""

RESPONSE_403_JSON = """
{
    "response": "string",
    "http_status_code": 1,
    "res_status": "INVALID_CREDENTIALS"
}
"""

