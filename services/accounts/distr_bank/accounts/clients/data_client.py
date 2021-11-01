import os
from contextlib import contextmanager

import requests
from distr_bank.accounts.clients.base_client import BaseClient
from distr_bank.accounts.models import Account
from distr_bank.accounts.utils import handle_response


class DataAuth(requests.auth.AuthBase):
    """
    Middleware to add authentication headers to the request
    """

    def __init__(self, user_agent: str, token: str = None):
        """
        DataAuth constructor

        Args:
            user_agent (str): agent to add to the request
            token (str, optional): token to add to the request
        """
        super().__init__()
        self.user_agent = user_agent
        self.token = token

    def __call__(self, request: requests.Request) -> requests.Response:
        """
        Method called internally by the requests lib

        Args:
            request (requests.Request): request to add info to

        Returns:
            requests.Response: request with additional info
        """
        request.headers["User-Agent"] = self.user_agent
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class DataClient(BaseClient):
    """
    Client to access the data service
    """

    def __init__(
        self,
        base_url: str = os.getenv("DATA_CLIENT_BASE_URL", "DATA_CLIENT_BASE_URL"),
        user_agent: str = os.getenv("DATA_CLIENT_USER_AGENT", "DATA_CLIENT_USER_AGENT"),
        token: str = None,
    ):
        """
        DataClient constructor

        Args:
            base_url (str, optional): base url of the service
                Defaults to the DATA_CLIENT_BASE_URL environment variable
            user_agent (str, optional): user agent to use for the requests
                Defaults to the DATA_CLIENT_USER_AGENT environment variable
            token (str, optional): authentication token to use
                Defaults to None
        """
        super().__init__()
        self.base_url = base_url
        self.token = token
        self.session.auth = DataAuth(user_agent=user_agent, token=token)

    @handle_response
    def get_account(self, account_id: int) -> Account:
        """
        Gets an account from the data service

        Args:
            account_id (int): account id

        Returns:
            Account: response from the service
        """
        return self.session.get(f"{self.base_url}/accounts/{account_id}")

    @handle_response
    def update_balance(self, account_id: int, balance: float) -> Account:
        """
        Updates the balance of an account

        Args:
            account_id (int): id of the account
            balance (float): balance to set for the account

        Returns:
            Account: updated account
        """
        with self.get_lock(account_id) as lock:
            return self.session.put(
                f"{self.base_url}/accounts/{account_id}",
                json={"balance": balance, "lock": lock},
            )

    @contextmanager
    def get_lock(self, account_id: int):
        """
        Context manager to lock and unlock an account

        Args:
            account_id (int): account to lock

        Yields:
            str: lock for the given account
        """
        lock = None
        try:
            response = self._lock_account(account_id)
            lock = response["lock"]
            yield lock
        finally:
            self._unlock_account(account_id, lock=lock)

    @handle_response
    def _lock_account(self, account_id: int) -> dict:
        return self.session.post(f"{self.base_url}/accounts/{account_id}/lock")

    @handle_response
    def _unlock_account(
        self, account_id: int, lock: str = None, force: bool = False
    ) -> dict:
        return self.session.post(
            f"{self.base_url}/accounts/{account_id}/unlock",
            json={"lock": lock, "force": force},
        )
