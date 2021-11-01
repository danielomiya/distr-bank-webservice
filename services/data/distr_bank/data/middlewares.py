import logging
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from itertools import count
from logging import FileHandler

from distr_bank.data.models.account import Account
from distr_bank.data.repos.base_repo import BaseRepo
from distr_bank.data.utils.http_error import create_error
from distr_bank.data.utils.logger_mixin import LoggerMixin
from flask import request


def with_account(repo: BaseRepo[Account]):
    """
    Decorator to get the account requested from the supplied repository
    or, if not found, return an error accordingly

    Args:
        repo (BaseRepo[Account]): repository

    Returns:
        callable: wrapped function
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(account_id, *args, **kwargs):
            account = repo.get(account_id)

            if not account:
                return create_error("account id not found", HTTPStatus.NOT_FOUND)

            return func(account, *args, **kwargs)

        return wrapped

    return wrapper


class TransactionLogger(LoggerMixin):
    """
    Class to implement logging of the transactions
    """

    def __init__(self) -> None:
        """
        TransactionLogger constructor
        """
        super().__init__()

        self.seq = count(1)
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        self.log.addHandler(FileHandler(f"logs/{now}.log", mode="w"))
        self.log.setLevel(logging.INFO)

    def __call__(self, func: callable) -> callable:
        """
        Works as an decorator to log successful responses to an external file

        Args:
            func (callable): function to be wrapped

        Returns:
            callable: wrapped function
        """

        @wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            account_id = kwargs.get("account_id")
            _, status_code = result
            requested_by = request.headers.get("X-Requested-By", "null")

            if 200 <= status_code < 300:
                body = request.get_json() or {}

                self.log.info(
                    "[%s] %d - - Origin: %s, Operation: %s, Account ID: %d, Value: %s",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    next(self.seq),
                    requested_by,
                    func.__name__,
                    account_id,
                    body.get("balance", "null"),
                )
            return result

        return wrapped
