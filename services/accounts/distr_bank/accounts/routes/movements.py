from http import HTTPStatus
from typing import Union

from distr_bank.accounts.clients.data_client import DataClient
from distr_bank.accounts.typing import Response
from distr_bank.accounts.utils import create_error
from flask import Blueprint, request
from requests import HTTPError

bp = Blueprint("movements", __name__)


@bp.post("/deposito/<int:account_id>/<int:amount>")
@bp.post("/deposito/<int:account_id>/<float:amount>")
def post_deposit(account_id: int, amount: Union[int, float]) -> Response:
    if amount <= 0:
        return create_error("amount to deposit must be > 0", HTTPStatus.BAD_REQUEST)

    client = DataClient(token=request.headers.get("Authorization"))
    account = client.get_account(account_id)

    balance = account["balance"] + amount

    return client.update_balance(account_id, balance), HTTPStatus.OK


@bp.post("/saque/<int:account_id>/<int:amount>")
@bp.post("/saque/<int:account_id>/<float:amount>")
def post_withdraw(account_id: int, amount: Union[int, float]) -> Response:
    if amount <= 0:
        return create_error("amount to withdraw must be > 0", HTTPStatus.BAD_REQUEST)

    client = DataClient(token=request.headers.get("Authorization"))
    account = client.get_account(account_id)

    if account["balance"] < amount:
        return create_error(
            "account doesn't have enough balance to withdraw", HTTPStatus.BAD_REQUEST
        )

    balance = account["balance"] - amount
    return client.update_balance(account_id, balance), HTTPStatus.OK


@bp.get("/saldo/<int:account_id>")
def get_balance(account_id: int) -> Response:
    client = DataClient(token=request.headers.get("Authorization"))

    try:
        account = client.get_account(account_id)
        return account, HTTPStatus.OK
    except HTTPError as err:
        if err.response.status_code != HTTPStatus.NOT_FOUND:
            raise
        return create_error("account not found", HTTPStatus.NOT_FOUND)


@bp.post("/transferencia/<int:source_id>/<int:destination_id>/<int:amount>")
@bp.post("/transferencia/<int:source_id>/<int:destination_id>/<float:amount>")
def post_transfer(
    source_id: int, destination_id: int, amount: Union[int, float]
) -> Response:
    if amount <= 0:
        return create_error("amount to transfer must be > 0", HTTPStatus.BAD_REQUEST)

    client = DataClient(token=request.headers.get("Authorization"))

    source_account = client.get_account(source_id)
    destination_account = client.get_account(destination_id)

    if source_account["balance"] < amount:
        return create_error(
            "source account doesn't have enough funds", HTTPStatus.BAD_REQUEST
        )

    source_balance = source_account["balance"] - amount
    destination_balance = destination_account["balance"] + amount

    source = client.update_balance(source_id, source_balance)
    destination = client.update_balance(destination_id, destination_balance)

    return {
        "source_account": source,
        "destination_account": destination,
        "amount_transferred": amount,
    }, HTTPStatus.OK
