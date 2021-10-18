import logging
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from itertools import count
from logging import FileHandler

from distr_bank.models.account import Account
from distr_bank.repos.base_repo import BaseRepo
from distr_bank.utils.http_error import create_error
from distr_bank.utils.logger_mixin import LoggerMixin
from flask import request


def with_account(repo: BaseRepo[Account]):
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
    def __init__(self):
        super().__init__()

        self.seq = count(1)
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        self.log.addHandler(FileHandler(f"logs/{now}.log", mode="w"))
        self.log.setLevel(logging.INFO)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            account_id = kwargs.get("account_id")
            _, status_code = result

            if 200 <= status_code < 300:
                body = request.get_json() or {}

                self.log.info(
                    "[%s] %d - - Origin: %d, Operation: %s, Account ID: %d, Value: %s",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    next(self.seq),
                    0,  # TODO: replace by the id of the server whom requested
                    func.__name__,
                    account_id,
                    body.get("balance", "null"),
                )
            return result

        return wrapped
