import json
import logging
import traceback
from functools import wraps
from pydantic import ValidationError
from http import HTTPStatus

from src.common.utils.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    TooManyRequestsError,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def standard_response(
    schema_class=None,
    success_message="Operación exitosa",
    success_status_code=HTTPStatus.OK,
):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                logger.info(
                    f"[Handler] Event received: {json.dumps(event, default=str)}"
                )

                body = json.loads(event.get("body", "{}"))
                if schema_class:
                    logger.info(f"[Handler] Validating schema: {schema_class.__name__}")
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

                logger.info(
                    f"[Handler] Successful response: {json.dumps(response_body, default=str)}"
                )

                return {
                    "statusCode": success_status_code,
                    "body": json.dumps(response_body, default=str),
                    "headers": {"Content-Type": "application/json"},
                }

            except ValidationError as ve:
                return _build_error_response(
                    HTTPStatus.BAD_REQUEST, "Datos inválidos", "ValidationError", ve
                )

            except ValueError as ve:
                return _build_error_response(
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                    "Error de validación",
                    "ValueError",
                    ve,
                )

            except UnauthorizedError as ue:
                return _build_error_response(
                    HTTPStatus.UNAUTHORIZED, "No autorizado", "UnauthorizedError", ue
                )

            except ForbiddenError as fe:
                return _build_error_response(
                    HTTPStatus.FORBIDDEN, "Acceso prohibido", "ForbiddenError", fe
                )

            except ConflictError as ce:
                return _build_error_response(
                    HTTPStatus.CONFLICT, "Conflicto de datos", "ConflictError", ce
                )

            except TooManyRequestsError as te:
                return _build_error_response(
                    HTTPStatus.TOO_MANY_REQUESTS,
                    "Demasiadas solicitudes",
                    "TooManyRequestsError",
                    te,
                )

            except Exception as e:
                logger.error("[Handler] Internal error:\n" + traceback.format_exc())
                return _build_error_response(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "Error interno",
                    "InternalError",
                    e,
                )

        return wrapper

    return decorator


def _build_error_response(
    status: HTTPStatus, message: str, error_type: str, exc: Exception
):
    logger.warning(f"[Handler] {error_type}: {str(exc)}")
    return {
        "statusCode": status.value,
        "body": json.dumps(
            {
                "success": False,
                "data": None,
                "message": message,
                "error": {
                    "code": status.value,
                    "type": error_type,
                    "message": str(exc),
                },
            },
            default=str,
        ),
        "headers": {"Content-Type": "application/json"},
    }
