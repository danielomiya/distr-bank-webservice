from functools import wraps
from http import HTTPStatus
from typing import Union

from distr_bank.accounts.typing import Response as FResponse
from requests import Response


def handle_response(func: callable) -> callable:
    """
    Given a function that returns an response, treats it accordingly

    Args:
        func (callable): function to wrap

    Returns:
        callable: wrapped function
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        response: Response = func(*args, **kwargs)

        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.RESET_CONTENT):
            return None

        if not response.ok:
            response.raise_for_status()

        return response.json()

    return wrapped


def create_error(message: str, status_code: Union[HTTPStatus, int]) -> FResponse:
    """
    Creates an error response

    Args:
        message (str): message of the error
        status_code (Union[HTTPStatus, int]): HTTP status of the error

    Returns:
        JsonObject: error response
    """
    body = {
        "status_code": status_code,
        "message": message,
    }
    return body, status_code
