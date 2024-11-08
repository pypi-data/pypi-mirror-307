"""Wrap all the result of the client."""
from typing import Protocol

import pandas as pd


class Result(Protocol):
    """Wrap the result of the client."""

    def to_pandas(self) -> pd.DataFrame:
        """Return the result as a pandas DataFrame."""
        ...

    def to_json(self) -> dict | list:
        """Return the result as a dict."""
        ...


class DictResult:
    """Wrap dict result."""

    def __init__(self, data: dict | list) -> None:
        """Generate the result class.

        Args:
            data (dict): data from the api
        """
        self._data = data

    def to_pandas(self) -> pd.DataFrame:
        """Return the result as a pandas DataFrame."""
        return pd.DataFrame(self._data)

    def to_json(self) -> dict | list:
        """Return the result as a dict."""
        return self._data


class PandasResult:
    """Wrap Pandas result."""

    def __init__(self, data: pd.DataFrame) -> None:
        """Generate the result class.

        Args:
            data (dict): data from the api
        """
        self._data = data

    def to_pandas(self) -> pd.DataFrame:
        """Return the result as a pandas DataFrame."""
        return self._data

    def to_json(self) -> dict | list:
        """Return the result as a dict."""
        return self._data.to_dict('records')
