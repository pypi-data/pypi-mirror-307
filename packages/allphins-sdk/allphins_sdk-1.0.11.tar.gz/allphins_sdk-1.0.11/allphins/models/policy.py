"""Policy model.

```
from allphins.models import Policy
```
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from allphins.client.client import Client
from allphins.client.result import DictResult
from allphins.client.result import Result
from allphins.const import ALLPHINS_API_URL
from allphins.const import GET
from allphins.const import ISO_8601
from allphins.models.base import BaseModel


class PolicyStatuses(str, Enum):
    """Policy status choices."""

    QUOTE = 'quote'
    WRITTEN = 'written'
    EXPIRED = 'expired'
    DECLINED = 'declined'
    NOT_TAKEN_UP = 'not_taken_up'
    WORK_IN_PROGRESS = 'work_in_progress'
    DELETED = 'deleted'


class Policy(BaseModel):
    """Policy model."""

    path = f'{ALLPHINS_API_URL}/policies/'

    @classmethod
    def live_policies(cls, policy_live_at: Optional[str] = None, filter_rule: Optional[str] = None) -> Result:
        """Get the live policies matching the policy_live_at date or the filter_rule.

        policy_live_at and filter_rule are mutually exclusive, but at least one of them must be provided.

        Args:
            policy_live_at (Optional str): Date of the policy live.
            filter_rule (Optional str): Filter rule to apply ('today', 'previous_1_1', 'next_1_1').

        Returns:
            list[dict]: List of policies on dict format.
        """
        url = ""
        if policy_live_at and filter_rule:
            raise ValueError('policy_live_at and filter_rule are mutually exclusive.')

        if not policy_live_at and not filter_rule:
            raise ValueError('policy_live_at or filter_rule must be provided.')

        if policy_live_at:
            try:
                datetime.strptime(policy_live_at, ISO_8601).date()
                url = f'{cls.path}?policy_live_at={policy_live_at}'
            except ValueError:
                raise ValueError(f'{policy_live_at} is not a valid ISO 8601 date.')

        if filter_rule:
            if filter_rule not in ['today', 'previous_1_1', 'next_1_1']:
                raise ValueError(f'{filter_rule} is not a valid filter rule.')
            url = f'{cls.path}?filter_rule={filter_rule}'

        return DictResult(Client().call_api(url, GET))

    @classmethod
    def from_portfolio_id(cls, portfolio_id: str) -> list['Policy']:
        """Instantiate a list of policy from a portfolio UUID.

        To get the dict representation of the portfolio policies, use the policies_to_dict() method of the portfolio.

        Args:
            portfolio_id (str): UUID of the portfolio.

        Returns:
            list[Policy]: List of policy instances.
        """
        from allphins.models.portfolio import Portfolio

        return Portfolio.from_id(portfolio_id).policy_models

    @classmethod
    def filtered_policies(cls, filters: dict) -> Result:
        """Get the policy ids matching the filters.

        Args:
            filters (dict): Filters to apply.

        Returns:
            Result: List of policy ids.
        """
        url = f'{cls.path}filter/?details=true&'
        for key, value in filters.items():
            url += f'{key}={value}&'
        return DictResult(Client().call_api(url[:-1], GET))
