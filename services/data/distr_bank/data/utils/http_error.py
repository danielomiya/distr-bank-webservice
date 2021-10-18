from http import HTTPStatus
from typing import Union

from distr_bank.data.typing import JsonObject


def create_error(message: str, status_code: Union[HTTPStatus, int]) -> JsonObject:
    body = {
        "status_code": status_code,
        "message": message,
    }
    return body, status_code
