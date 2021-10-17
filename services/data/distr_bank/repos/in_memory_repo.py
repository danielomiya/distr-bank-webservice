from collections.abc import Sized
from typing import Dict

from distr_bank.repos.base_repo import BaseRepo, T
from distr_bank.utils.logger_mixin import LoggerMixin


class InMemoryRepo(BaseRepo[T], LoggerMixin, Sized):
    def __init__(self):
        self.size: int = 0
        self.items: Dict[int, T] = {}
        super().__init__()

    def add(self, item: T) -> int:
        _id = self.size
        item.id = _id

        self.log.debug("Assgined id %d to '%s'", _id, item.as_dict())

        self.items[_id] = item
        self.size += 1
        return _id

    def get(self, _id: int, *, fallback: T = None) -> T:
        return self.items.get(_id, fallback)

    def __len__(self) -> int:
        return self.size
