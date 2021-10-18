from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class Entity(metaclass=ABCMeta):
    id: int = None

    @abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError()
