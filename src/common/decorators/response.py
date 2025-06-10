import json
import logging
import traceback
from functools import wraps
from pydantic import ValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def standard_response(
    schema_class=None,
    success_message="Operación exitosa",
    validation_error_message="Datos inválidos",
    internal_error_message="Error interno",
    success_status_code=200,
    validation_error_status_code=400,
    internal_error_status_code=500
):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                body = json.loads(event.get("body", "{}"))
                if schema_class:
                    schema_class(**body)

                result = func(event, context)

                response_body = {
                    "success": True,
                    "data": None,
                    "message": success_message,
                    "error": None,
                }

                if isinstance(result, dict):
                    if "pagination" in result:
                        response_body["data"] = result.get("data", [])
                        response_body["pagination"] = result["pagination"]
                    else:
                        response_body["data"] = result
                else:
                    response_body["data"] = result

                return {
                    "statusCode": success_status_code,
                    "body": json.dumps(response_body),
                    "headers": {"Content-Type": "application/json"},
                }

            except ValidationError as ve:
                return {
                    "statusCode": validation_error_status_code,
                    "body": json.dumps({
                        "success": False,
                        "data": None,
                        "message": validation_error_message,
                        "error": {
                            "code": validation_error_status_code,
                            "type": "ValidationError",
                            "message": str(ve),
                            "details": ve.errors(),
                        },
                    }),
                    "headers": {"Content-Type": "application/json"},
                }

            except Exception as e:
                logger.error(traceback.format_exc())
                return {
                    "statusCode": internal_error_status_code,
                    "body": json.dumps({
                        "success": False,
                        "data": None,
                        "message": internal_error_message,
                        "error": {
                            "code": internal_error_status_code,
                            "type": "InternalError",
                            "message": str(e),
                        },
                    }),
                    "headers": {"Content-Type": "application/json"},
                }

        return wrapper
    return decorator
