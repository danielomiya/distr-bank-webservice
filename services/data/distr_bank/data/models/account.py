from dataclasses import dataclass

from distr_bank.data.models.entity import Entity
from distr_bank.data.models.lockable import Lockable


@dataclass
class Account(Entity, Lockable):
    """
    Account entity model
    """

    balance: float = 0.0

    def as_dict(self) -> dict:
        """
        Gets this account instance as dict

        Returns:
            dict: this instance's representation as dict
        """
        return {
            "id": self.id,
            "balance": self.balance,
            "is_locked": self.is_locked,
        }
