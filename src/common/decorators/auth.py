import json
import logging
from functools import wraps
from src.common.auth.jwt import decode_jwt_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def require_auth(expected_purpose=None):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            headers = event.get("headers", {})
            auth_header = headers.get("Authorization") or headers.get("authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return {
                    "statusCode": 401,
                    "body": json.dumps(
                        {
                            "success": False,
                            "data": None,
                            "message": "Authorization token missing or invalid",
                            "error": {
                                "code": 401,
                                "type": "Unauthorized",
                                "message": "Missing Bearer token",
                            },
                        }
                    ),
                    "headers": {"Content-Type": "application/json"},
                }

            token = auth_header.split(" ")[1]
            logger.info(f"Received token: {token}")

            try:
                payload = decode_jwt_token(token)
                logger.info(f"Decoded payload: {payload}")

                if expected_purpose and payload.get("purpose") != expected_purpose:
                    return {
                        "statusCode": 403,
                        "body": json.dumps(
                            {
                                "success": False,
                                "data": None,
                                "message": "Invalid token purpose",
                                "error": {
                                    "code": 403,
                                    "type": "TokenPurposeError",
                                    "message": f"Expected '{expected_purpose}', got '{payload.get('purpose')}'",
                                },
                            }
                        ),
                        "headers": {"Content-Type": "application/json"},
                    }

                event["auth"] = payload
                return func(event, context)

            except Exception as e:
                logger.error(f"JWT decode error: {str(e)}")
                return {
                    "statusCode": 401,
                    "body": json.dumps(
                        {
                            "success": False,
                            "data": None,
                            "message": "Invalid or expired token",
                            "error": {
                                "code": 401,
                                "type": "TokenError",
                                "message": str(e),
                            },
                        }
                    ),
                    "headers": {"Content-Type": "application/json"},
                }

        return wrapper

    return decorator
