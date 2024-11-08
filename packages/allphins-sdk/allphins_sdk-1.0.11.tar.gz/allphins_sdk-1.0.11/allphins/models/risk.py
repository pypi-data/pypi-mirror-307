"""Risk model."""
from allphins.client import Client
from allphins.client.result import DictResult
from allphins.client.result import Result
from allphins.const import ALLPHINS_API_URL
from allphins.const import POST
from allphins.models.base import BaseModel


class Risk(BaseModel):
    """Risk model."""

    path = f'{ALLPHINS_API_URL}/risks/list_details/'
    PAGE_SIZE = 5000

    @classmethod
    def filtered_risk(cls, filters: dict) -> Result:
        """Get the filtered risks.

        Args:
            filters (dict): Filters to apply.

        Returns:
            Risk: Risk object.
        """
        risks = Client().call_api_with_pagination(cls.path, POST, json=filters, page_size=Risk.PAGE_SIZE)
        return DictResult(risks)
