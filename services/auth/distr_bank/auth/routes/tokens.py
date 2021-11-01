from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from distr_bank.auth.utils import create_error
from flask import Blueprint, request

bp = Blueprint("tokens", __name__)


def get_claims(
    user: str,
    reference_time: datetime = None,
    expires_in: timedelta = timedelta(hours=2),
) -> dict:
    if not reference_time:
        reference_time = datetime.utcnow()

    expires_at = reference_time + expires_in
    issuer = "auth service"
    audience = "business client"

    return {
        "exp": expires_at,
        "iss": issuer,
        "aud": audience,
        "sub": user,
        "iat": reference_time,
    }


@bp.post("/token")
def gen_token():
    json = request.get_json() or {}

    if "username" not in json or "password" not in json:
        return create_error(
            "missing username or password in body", HTTPStatus.BAD_REQUEST
        )

    if json["username"] != "admin" or json["password"] != "admin":
        return create_error("wrong username or password", HTTPStatus.BAD_REQUEST)

    claims = get_claims(user=json["username"])
    token = jwt.encode(claims, key="secret", algorithm="HS256")

    return {"token": token, "expires_at": claims["exp"].isoformat("T")}, HTTPStatus.OK
