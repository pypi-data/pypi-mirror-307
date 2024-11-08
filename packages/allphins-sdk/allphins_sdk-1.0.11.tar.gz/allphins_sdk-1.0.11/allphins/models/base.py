"""Base class for models."""
from typing import Any
from typing import TypeVar

from allphins.client.client import Client
from allphins.client.result import DictResult
from allphins.client.result import Result
from allphins.const import GET

T = TypeVar('T', bound='BaseModel')


class BaseModel:
    """This class is the base for all the models.

    It serves as a wrapper for all operations (API calls) that can be done on the model.
    All class have a method to_dict that returns the data of the model as a dict through a GET query to the API.

    Attributes:
        _cache: basic cache for the API calls based on the url called
        _client: The client to use for API calls.
        _model_id: The id of the model.
    """

    path: str = None

    def __init__(self, model_id: str = None):
        """Initialize the model."""
        self._cache: dict = {}
        self._client = Client()
        self._model_id = model_id

    @property
    def _item_path(self) -> str:
        """Get the path of the model.

        Returns:
            str: The path of the model.
        """
        return f'{self.path}{self._model_id}/'

    @classmethod
    def from_id(cls: type[T], model_id: str) -> T:
        """Instantiate a Model from its id.

        Args:
            model_id (str): id of the model.

        Returns:
            BaseModel: Instance of the model.
        """
        return cls(model_id)

    def get_item(self) -> Result:
        """Get the data of the model in a dict format.

        Returns:
            dict: Dict containing the response of the API call.
        """
        return DictResult(self._get(self._item_path))

    def _get(self, url: str) -> Any:
        """Perform a GET request on the API.

        Use a basic cache to avoid calling the API multiple times for the same url.

        Args:
            url (str): The url to call.

        Returns:
            Any: The response of the API call.
        """
        if url not in self._cache:
            self._cache[url] = self._client.call_api(url, GET)
        return self._cache[url]
