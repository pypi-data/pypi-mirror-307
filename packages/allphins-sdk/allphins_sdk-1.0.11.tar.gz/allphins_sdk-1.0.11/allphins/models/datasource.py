"""Datasource model.

```
from allphins.models import Datasource
```
"""
import pandas as pd

from allphins.client.result import PandasResult
from allphins.client.result import Result
from allphins.const import ALLPHINS_API_URL
from allphins.models.base import BaseModel
from allphins.utils import validate_uuid4


class Datasource(BaseModel):
    """Datasource model."""

    path = f'{ALLPHINS_API_URL}/datasources/'

    def __init__(self, datasource_id: str):
        """Instantiate a Datasource from a datasource UUID.

        Args:
            datasource_id (str): UUID of the datasource.

        Raises:
            ValueError: If the datasource_id is not a valid UUID.
        """
        if not validate_uuid4(datasource_id):
            raise ValueError(f'{datasource_id} is not a valid UUID.')

        super().__init__(datasource_id)

    @classmethod
    def from_portfolio_id(cls, portfolio_id: str) -> list['Datasource']:
        """Instantiate a list of Datasource from a portfolio UUID.

        To get the dict representation of the portfolio datasource,
        use the datasources_to_dict() method of the portfolio.

        Args:
            portfolio_id (str): UUID of the portfolio.

        Returns:
            list[Datasource]: List of datasource.
        """
        from allphins.models.portfolio import Portfolio

        return Portfolio.from_id(portfolio_id).datasource_models

    def parquet_risks(self) -> Result:
        """Get the parquet risks of the datasource as a pandas DataFrame.

        Returns:
            DataFrame: Pandas DataFrame containing the risks.
        """
        response = self._get(f'{self.path}{self._model_id}/parquet_signed_urls/?type=RISKS')
        risks_urls = response.get('results', [])
        risks_table = pd.concat(pd.read_parquet(url) for url in risks_urls)
        return PandasResult(risks_table)
