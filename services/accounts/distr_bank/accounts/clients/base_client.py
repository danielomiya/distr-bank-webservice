from abc import ABCMeta

import requests


class BaseClient(metaclass=ABCMeta):
    """
    Base client to implement API clients
    """

    def __init__(self) -> None:
        """
        BaseClient constructor
        """
        self.session = requests.Session()
