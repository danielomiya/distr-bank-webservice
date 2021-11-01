from typing import TypedDict


class Account(TypedDict):
    id: int
    balance: float
    is_locked: bool
