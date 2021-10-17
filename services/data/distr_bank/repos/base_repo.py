from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from distr_bank.models.entity import Entity

T = TypeVar("T", Entity, object)


class BaseRepo(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def add(self, item: T) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get(self, _id: int, *, fallback: T = None) -> T:
        raise NotImplementedError()
