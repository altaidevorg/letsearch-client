import httpx
from .types import (
    CollectionInfo,
    HealthcheckResponse,
    ErrorResponse,
    CollectionsResponse,
    SearchResponse,
)
from typing import Dict

DEFAULT_BASE_URL = "http://localhost:7898"


class LetsearchClient:
    """
    A client for interacting with the Letsearch API.

    Args:
        letsearch_url (str): The base URL of the Letsearch API. Defaults to "http://localhost:7898".
        timeout (int | None): Request timeout in seconds. Defaults to None.
        raise_for_status (bool): Whether to raise exceptions for HTTP errors. Defaults to True.
    """

    def __init__(
        self,
        letsearch_url: str = "http://localhost:7898",
        timeout: int | None = None,
        raise_for_status: bool = True,
    ):
        self.base_url = (
            letsearch_url.rstrip("/")
            if isinstance(letsearch_url, str)
            else DEFAULT_BASE_URL
        )
        self.client = httpx.Client(base_url=self.base_url, timeout=timeout)
        self.raise_for_status = raise_for_status

    def __enter__(self):
        """
        Enter the runtime context for the client.
        Returns:
            LetsearchClient: The client instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context, closing the client.
        """
        self.close()

    def close(self) -> None:
        """
        Close the underlying HTTP client and release resources.
        """
        self.client.close()

    def _request(
        self, endpoint: str, method: str | None = None, body: Dict | None = None
    ) -> Dict | ErrorResponse:
        """
        Internal method to send HTTP requests.

        Args:
            endpoint (str): API endpoint (relative to the base URL).
            method (str | None): HTTP method, either 'get' or 'post'. Defaults to None.
            body (Dict | None): Request body for POST requests. Defaults to None.

        Returns:
            Dict | ErrorResponse: The parsed JSON response or an ErrorResponse in case of an error.
        """
        try:
            res = (
                self.client.get(endpoint)
                if method == "get"
                else self.client.post(endpoint, json=body)
            )
            if self.raise_for_status:
                res.raise_for_status()
            return res.json()["data"]
        except httpx.HTTPStatusError as e:
            if self.raise_for_status:
                raise e
            res = e.response.json()
            return ErrorResponse(message=res["message"])

    def healthcheck(self) -> HealthcheckResponse | ErrorResponse:
        """
        Check the health of the Letsearch API.

        Returns:
            HealthcheckResponse | ErrorResponse: Healthcheck information or an error response.
        """
        res = self._request("/", "get")
        if isinstance(res, ErrorResponse):
            return res
        else:
            return HealthcheckResponse(version=res["version"], status=res["status"])

    def get_collections(self) -> CollectionsResponse:
        """
        Retrieve information about all collections in Letsearch.

        Returns:
            CollectionsResponse: A response containing the list of collections.
        """
        res = self._request("/collections", "get")
        if isinstance(res, ErrorResponse):
            return res
        else:
            result = CollectionsResponse.model_validate(res)
            return result

    def get_collection(self, collection_name: str) -> CollectionInfo:
        """
        Retrieve information about a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            CollectionInfo: Information about the specified collection.
        """
        res = self._request(f"/collections/{collection_name}", "get")
        if isinstance(res, ErrorResponse):
            return res
        else:
            result = CollectionInfo.model_validate(res)
            return result

    def search(
        self, collection_name: str, column_name: str, query: str, limit=10
    ) -> SearchResponse:
        """
        Perform a search query on a specific collection.

        Args:
            collection_name (str): The name of the collection to search in.
            column_name (str): The column to search within.
            query (str): The search query.
            limit (int): The maximum number of results to return. Defaults to 10.

        Returns:
            SearchResponse: The search results or an error response.
        """
        body = {"column_name": column_name, "query": query, limit: limit}
        res = self._request(f"/collections/{collection_name}/search", "post", body=body)
        if isinstance(res, ErrorResponse):
            return res
        else:
            result = SearchResponse.model_validate(res)
            return result
