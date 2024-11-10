# pointofpresence/search_method.py

from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientSearch(APIClientBase):
    """Extension of APIClientBase with search functionality for datasets."""

    def search_datasets(self, terms, server="local"):
        """
        Search datasets by a list of terms.

        :param terms: A list of terms to search for in the datasets.
        :param server: Specify the server to search on: 'local' or 'global'.
        :return: List of matching datasets.
        :raises ValueError: If the search fails.
        """
        url = f"{self.base_url}/search"
        params = {"terms": terms, "server": server}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract error details if available
            error_detail = response.json().get("detail", str(e))
            raise ValueError(f"Error searching for datasets: {error_detail}")
