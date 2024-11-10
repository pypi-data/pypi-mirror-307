# pointofpresence/client_base.py

import requests


class APIClientBase:
    """Base class for the API client."""

    def __init__(
        self, base_url: str, username: str = None, password: str = None
    ):
        """
        Initialize the API client.

        :param base_url: Base URL of the API.
        :param username: Username for authentication.
        :param password: Password for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None

        # Validate that both username and password are provided together
        # or not at all
        if (username and not password) or (password and not username):
            raise ValueError(
                "Both username and password must be provided together."
            )

        if not username and not password:
            self._check_api_availability()
        if username and password:
            self.get_token(username, password)

    def _check_api_availability(self):
        """
        Check if the API is reachable by making a GET request to the base URL.
        Raises a ValueError if the connection fails or the response is not 200.
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise ValueError(
                f"Failed to connect to the API at {self.base_url}. "
                "Please check if the URL is correct and reachable."
            )
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                "API connection check failed with "
                f"status code {response.status_code}: {http_err}"
            )
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while attempting to connect "
                f"to the API: {req_err}"
            )

    def get_token(self, username: str, password: str):
        """
        Obtain authentication token.

        :param username: Username for authentication.
        :param password: Password for authentication.
        """
        url = f"{self.base_url}/token"
        try:
            response = self.session.post(
                url, data={"username": username, "password": password}
            )
            response.raise_for_status()
            self.token = response.json().get("access_token")
            if not self.token:
                raise ValueError(
                    "Authentication failed: No access token received."
                )
            # Update session headers with the token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                f"Failed to connect to the API at {self.base_url}. "
                "Please check if the URL is correct and reachable."
            )
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise ValueError(
                    "Authentication failed: Invalid username or password."
                ) from http_err
            else:
                raise ValueError(
                    f"HTTP error occurred: {http_err}"
                ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while attempting to obtain "
                f"the token: {req_err}"
            ) from req_err
