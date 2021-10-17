from functools import wraps
from http import HTTPStatus

from distr_bank.models.account import Account
from distr_bank.repos.base_repo import BaseRepo
from distr_bank.utils.http_error import create_error


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
