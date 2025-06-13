import json
from src.schemas.auth_schemas import UserLoginSchema
from src.services.login_service import login_user
from src.common.decorators.response import standard_response


@standard_response(schema_class=UserLoginSchema)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    username = body["username"]
    password = body["password"]

    user = login_user(username, password)

    if not user:
        raise ValueError("Credenciales inválidas")

    return user
