"""Portfolio model.

```
from allphins.models import Portfolio
```
"""

from allphins.client.client import Client
from allphins.client.result import DictResult
from allphins.client.result import Result
from allphins.const import ALLPHINS_API_URL
from allphins.const import GET
from allphins.models.base import BaseModel
from allphins.models.datasource import Datasource
from allphins.models.policy import Policy
from allphins.utils import validate_uuid4


class Portfolio(BaseModel):
    """Portfolio model."""

    path = f'{ALLPHINS_API_URL}/portfolios/'

    def __init__(self, portfolio_id: str):
        """Instantiate a Portfolio from a portfolio UUID.

        Args:
            portfolio_id (str): UUID of the portfolio.

        Raises:
            ValueError: If the portfolio_id is not a valid UUID.
        """
        if not validate_uuid4(portfolio_id):
            raise ValueError(f'{portfolio_id} is not a valid UUID.')

        super().__init__(portfolio_id)

    @classmethod
    def all(cls) -> Result:
        """Get all the portfolios.

        Returns:
            list[dict]: List of the portfolios dict representation.
        """
        return DictResult(Client().call_api(Portfolio.path, GET))

    @property
    def policy_models(self) -> list[Policy]:
        """Get the Policy list of the Portfolio.

        To get the data of the policies as a dict, use the policies_to_dict() method.

        Returns:
            list[Policy]: List of Policy instances.
        """
        item = self.get_item().to_json()
        if isinstance(item, dict):
            return [Policy.from_id(policy['id']) for policy in item['policies']]
        raise TypeError('The portfolio is not a dict.')

    @property
    def datasource_models(self) -> list[Datasource]:
        """Get the Datasource list of the Portfolio.

        To get the data of the datasources as a dict, use the datasources_to_dict() method.

        Returns:
            list[Datasource]: List of Datasource instances.
        """
        datasources_details = self._get(f'{self._item_path}datasources/')
        return [Datasource.from_id(datasource['id']) for datasource in datasources_details]

    def policies(self) -> Result:
        """Get the policies of the portfolio.

        Returns:
            dict: Dict representation of the policies.
        """
        item = self.get_item().to_json()
        if isinstance(item, dict):
            return DictResult(item['policies'])
        raise TypeError('The portfolio is not a dict.')

    def datasources(self) -> Result:
        """Get the datasources of the portfolio.

        Returns:
            dict: Dict representation of the datasources.
        """
        return DictResult(self._get(f'{self._item_path}datasources/'))
