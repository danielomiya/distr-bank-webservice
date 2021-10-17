from abc import ABCMeta
from dataclasses import dataclass
from uuid import uuid4

from distr_bank.exceptions import LockException


@dataclass
class Lockable(metaclass=ABCMeta):
    """
    Mixin to enable basic handling of a lockable resource
    """

    _lock: str = None

    @property
    def is_locked(self) -> bool:
        return self._lock is not None

    def acquire(self) -> str:
        """
        Acquires an id to edit the resource

        Raises:
            LockException: if the resource is already locked

        Returns:
            str: id
        """
        if self.is_locked:
            raise LockException("Cannot acquire lock")
        self._lock = uuid4().hex
        return self._lock

    def release(self) -> None:
        """
        Releases the lock

        Raises:
            LockException: if the resource is not locked
        """
        if not self.is_locked:
            raise LockException("Cannot release lock")
        self._lock = None

    def verify_lock(self, id_: str) -> bool:
        """
        Verifies if the given id can edit the resource

        Args:
            id_ (str): an id to be validated

        Returns:
            bool: whether the given id is valid
        """
        return self._lock == id_
