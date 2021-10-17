from http import HTTPStatus

from distr_bank.middlewares import with_account
from distr_bank.models.account import Account
from distr_bank.repos.base_repo import BaseRepo
from distr_bank.repos.in_memory_repo import InMemoryRepo
from distr_bank.typing import Response
from distr_bank.utils.http_error import create_error
from flask import Blueprint, request

bp = Blueprint("accounts", __name__)
accounts_repo: BaseRepo[Account] = InMemoryRepo()


@bp.post("/accounts/<int:account_id>/lock")
@with_account(accounts_repo)
def post_lock(account: Account) -> Response:
    if account.is_locked:
        return create_error("resource already locked", HTTPStatus.CONFLICT)

    hash = account.acquire()

    return {
        "id": account.id,
        "is_locked": True,
        "lock": hash,
    }, HTTPStatus.OK


@bp.post("/accounts/<int:account_id>/unlock")
@with_account(accounts_repo)
def post_unlock(account: Account) -> Response:
    if not account.is_locked:
        return create_error("resource already unlocked", HTTPStatus.CONFLICT)

    json = request.get_json() or {}
    lock = json.get("lock")
    force = json.get("force", False)

    if force or (lock and account.verify_lock(lock)):
        account.release()
        return {
            "id": account.id,
            "is_locked": False,
        }, HTTPStatus.OK

    return create_error("could not unlock resource", HTTPStatus.BAD_REQUEST)


@bp.get("/accounts/<int:account_id>")
@with_account(accounts_repo)
def get_account(account: Account) -> Response:
    return account.as_dict(), HTTPStatus.OK


@bp.put("/accounts/<int:account_id>")
@with_account(accounts_repo)
def put_account(account: Account) -> Response:
    json = request.get_json()
    lock = json.get("lock")

    if not lock or not account.verify_lock(lock):
        return create_error(
            "either lock not supplied or invalid", HTTPStatus.BAD_REQUEST
        )

    account.balance = json.get("balance", account.balance)
    return account.as_dict(), HTTPStatus.OK


@bp.post("/accounts/_seed")
def seed():
    for _ in range(1000):
        accounts_repo.add(Account(balance=1000.0))
    return "", HTTPStatus.NO_CONTENT


@bp.post("/accounts/_clear")
def clear():
    if not isinstance(accounts_repo, InMemoryRepo):
        return "", HTTPStatus.INTERNAL_SERVER_ERROR

    accounts_repo.items.clear()
    return "", HTTPStatus.NO_CONTENT
