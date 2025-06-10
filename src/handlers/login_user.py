import json
from src.schemas.auth_schemas import UserLoginSchema
from src.services.login_service import login_user
from src.common.auth.jwt import create_jwt_token
from src.common.decorators.response import standard_response


@standard_response(schema_class=UserLoginSchema)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    username = body["username"]
    password = body["password"]

    user = login_user(username, password)

    if not user:
        raise Exception("Credenciales inválidas")

    token = create_jwt_token(
        {"sub": user["username"], "role": "user"}, expires_in_minutes=60
    )

    return {
        "username": user["username"],
        "name": user["name"],
        "rol": "User",
        "token": token,
    }
