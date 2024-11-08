"""This module provides methods to interact with the allphins API."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from pandas import DataFrame

from allphins.const import ISO_8601
from allphins.models import Policy
from allphins.models import Portfolio
from allphins.models import Risk
from allphins.models import ScenarioList
from allphins.models.policy import PolicyStatuses
from allphins.utils import validate_uuid4

logger = logging.getLogger(__name__)


def get_portfolios() -> DataFrame:
    """Get all the portfolios.

    Returns:
        dataframe of the portfolios' representation.

    ##### Response structure
    | Attribute           | Type        | Description                                                                                                                        |
    | ------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
    | `id`                | _UUID_      | Unique identifier for the object.                                                                                                  |
    | `name`              | _string_    | Name of the portfolio.                                                                                                             |
    | `created_at`        | _timestamp_ | Creation date.                                                                                                                     |
    | `updated_at`        | _timestamp_ | Last update date.                                                                                                                  |
    | `data_update_time ` | _timestamp_ | Last data update date.                                                                                                             |
    | `renewal_date`      | _timestamp_ | Next renewal date.                                                                                                                 |
    | `premium`           | _int_       | Premium in USD.                                                                                                                    |
    | `max_exposure`      | _float_     | Maximum exposure on the portfolio (based on enterd policies).                                                                      |
    | `policies`          | _list_      | List of policies.                                                                                                                  |
    | `client`            | _int_       | ID of the client.                                                                                                                  |
    | `client_name`       | _string_    | Name of the client                                                                                                                 |
    | `timeline`          | _string_    | Status of the portofolio (expired, active, etc...)                                                                                 |
    | `renewal`           | _string_    | ID of the next portfolio.                                                                                                          |
    | `portfolio_class`   | _string_    | Line of business of the portfolio.                                                                                                 |
    | `year_of_account`   | _int_       | Year of account.                                                                                                                   |
    | `transaction`       | _string_    | Type of transaction: `pre_inward`, `inward`, `selfward`, `outward`.                                                                |
    | `datasource`        | _list_      | list of datasources

    """
    logger.info('Fetching portfolios from Allphins API.')
    return Portfolio.all().to_pandas()


def get_policies(
    portfolio_id: Optional[uuid.UUID] = None,
    status: Optional[str] = 'written',
    validity: Optional[str] = 'today',
) -> DataFrame:
    """Get the policies, using filtering parameters.

    Args:
        portfolio_id (Optional[uuid.UUID]): UUID of the portfolio.
        status (Optional[str]): Status of the policy
        validity (Optional[str]): Validity of the policy

    ##### Allowed values
    | Status             | Validity                                                  |
    |--------------------|-----------------------------------------------------------|
    | `quote`            | `today` _(policies valid today)_                          |
    | `written`          | `previous_1_1` _(policies valid previous 1st of January)_ |
    | `expired`          |                                                           |
    | `declined`         |                                                           |
    | `not_taken_up`     |                                                           |
    | `work_in_progress` |                                                           |
    | `deleted`          |                                                           |

    To disable `status` or `validity` filtering, explicitly set the value to `None`.

    <br/>

    Returns:
        dataframe of the policies' representation.

    ##### Response structure
    | Attribute                              | Type       | Description                                                        |
    | -------------------------------------- | ---------- | ------------------------------------------------------------------ |
    | `id`                                   | _int_      | Unique identifier for the object.                                  |
    | `type`                                 | _string_   | Policy type: `direct`, `excess_of_loss` or `quota_share`.          |
    | `portfolio`                            | _string_   | ID of the portfolios object.                                       |
    | `portfolio_name`                       | _string_   | Name of the portfolio                                              |
    | `premium_100`                          | _float_    | Premium at 100% share.                                             |
    | `premium_currency`                     | _string_   | Premium currency.                                                  |
    | `usd_premium_100`                      | _float_    | USD Premium at 100% share.                                         |
    | `benefits`                             | _list_     | List of the benefits.                                              |
    | `limit`                                | _float_    | Policy limit.                                                      |
    | `limit_currency`                       | _string_   | Limit currency.                                                    |
    | `usd_limit`                            | _float_    | USD limit.                                                         |
    | `excess`                               | _float_    | Policy excess.                                                     |
    | `excess_currency`                      | _string_   | Excess currency.                                                   |
    | `start_date`                           | _datetime_ | Start date of the policy.                                          |
    | `end_date`                             | _datetime_ | End date of the policy.                                            |
    | `dates`                                | _json_     | Json representation of the start date and end date.                |
    | `risk_attached`                        | _bool_     | Is it a risk attaching policy.                                     |
    | `share`                                | _float_    | Policy share.                                                      |
    | `combined_ratio`                       | _float_    | Combined ratio of the policy.                                      |
    | `status`                               | _string_   | Policy status: `written`, `quote`, `declined`, `not_taken_up`.     |
    | `reinstatement`                        | _float_    | Reinstatement percentage.                                          |
    | `reference`                            | _string_   | Policy reference.                                                  |
    | `description`                          | _float_    | Policy description.                                                |
    | `tags`                                 | _list_     | List of tags.                                                      |
    | `rules`                                | _list_     | Sublimit rules.                                                    |
    | `outward_filter`                       | _json_     | Outward filters.                                                   |
    | `rol`                                  | _float_    | Rol of the policy.                                                 |
    | `client_id`                            | _int_      | Id of the client.                                                  |
    | `client_name`                          | _string_   | Name of the client                                                 |
    | `annual_aggregate_deductible_currency` | _string_   | Annual aggregate deductible currency.                              |
    | `annual_aggregate_deductible`          | _float_    | Annual aggregate deductible.                                       |

    """
    filters: dict = {}

    if portfolio_id:
        if not validate_uuid4(portfolio_id):
            raise ValueError(f'{portfolio_id} is not a valid UUID.')
        filters['portfolio_id'] = portfolio_id

    if validity:
        if validity not in ['today', 'previous_1_1']:
            raise ValueError(f'{validity} is not a valid filter rule.')
        filters['filter_rule'] = validity

    if status:
        try:
            PolicyStatuses(status)
        except ValueError:
            raise ValueError(f'{status} is not a valid status.')
        filters['status'] = status

    logger.info('Fetching policies from Allphins API.')

    return Policy.filtered_policies(filters).to_pandas()


def get_risks(
    portfolio_id: Optional[uuid.UUID] = None,
    datasource_id: Optional[uuid.UUID] = None,
    scenario_id: Optional[int] = None,
) -> DataFrame:
    """Get the risks, using filtering parameters.

    At least one of the parameters must be provided.

    Fetching the risks from the API could take a while, depending on the amount of data to retrieve.

    Args:
        portfolio_id (Optional[uuid.UUID]): UUID of the portfolio.
        datasource_id (Optional[uuid.UUID]): UUID of the datasource_id.
        scenario_id (Optional[int]): id of the scenario_id.

    Returns:
        dataframe of the risks' representation.

    ##### Response structure
    | Attribute              | Type        | Description                                                  |
    | ---------------------- | ----------- | ------------------------------------------------------------ |
    | `id`                   | _int_       | Unique identifier for the object.                            |
    | `name`                 | _string_    | Name of the risk.                                            |
    | `start_date`           | _timestamp_ | Start date.                                                  |
    | `end_date`             | _timestamp_ | End date.                                                    |
    | `dates`                | _json_      | Object representation of the start date and end date.        |
    | `gross_exposure`       | _float_     | Gross Exposure in USD.                                       |
    | `gross_exposure_raw`   | _float_     | Gross Exposure.                                              |
    | `portfolio_id`         | _string_    | ID of the portfolio object.                                  |
    | `portfolio_name`       | _string_    | Name of the portfolio.                                       |
    | `portfolio_class`      | _string_    | Line of business of the portfolio.                           |
    | `extra_fields`         | _json_      | Raw data from the risk import.                               |
    | `mapped_data`          | _json_      | Mapped data from the risk import.                            |
    | `assured_interest`     | _float_     | Assured interest.                                            |
    | `is_assured_interest`  | _bool_      | Assured interest.                                            |
    | `mute`                 | _bool_      | Is the risk muted or not.                                    |
    | `attributes`           | _list_      | List of attributes for this risk.                            |
    | `attributes_array`     | _list_      | List of ids of the attributes for this risk.                 |
    | `cedant_share`         | _float_     | Cedant share.                                                |
    | `limit_100`            | _float_     | Limit at 100%.                                               |
    | `excess`               | _float_     | Excess.                                                      |
    | `premium_100`          | _float_     | Premium at 100%.                                             |
    | `currency`             | _string_    | Currency.                                                    |
    | `attributes`           | _list_      | List of attributes for this risk.                            |
    | `datasource_id`        | _string_    | ID of the datasource object.                                 |
    | `datasource_name`      | _string_    | Name of the datasource.                                      |

    """
    if not any([portfolio_id, datasource_id, scenario_id]):
        raise ValueError('At least one of the parameters must be provided.')

    filters: dict = {}

    if portfolio_id:
        if not validate_uuid4(portfolio_id):
            raise ValueError(f'{portfolio_id} is not a valid UUID.')
        filters['portfolios'] = portfolio_id

    if datasource_id:
        if not validate_uuid4(datasource_id):
            raise ValueError(f'{datasource_id} is not a valid UUID.')
        filters['datasource_id'] = datasource_id

    if scenario_id:
        if not (isinstance(scenario_id, int) and scenario_id > 0):
            raise ValueError(f'{scenario_id} is not a valid scenario_id.')
        filters['scenario_id'] = scenario_id

    logger.info('Fetching risks from Allphins API.')

    return Risk.filtered_risk(filters).to_pandas()


def get_aggregation(
    scenariolist_id: uuid.UUID,
    policies: list[int],
    computation_date: Optional[str] = datetime.now().strftime('%Y-%m-%d'),
) -> DataFrame:
    """Get the aggregation for the given scenariolist and policies at the given computation date.

    Args:
        scenariolist_id (uuid.UUID): UUID of the scenario list.
        policies (list[int]): List of policy ids.
        computation_date (Optional[str]): Date of the computation, default to today.

    Returns:
        dataframe of the aggregation's representation.

    ##### Response structure
    | Attribute           | Type        | Description                                                                                                                        |
    | ------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
    | `id`                | _int_       | Unique identifier for the scenario.                                                                                                |
    | `name`              | _string_    | Name of the scenario.                                                                                                              |
    | `attributes`        | _list_      | Attributes list of the scenario.                                                                                                   |
    | `meta_data`         | _list_      | Meta data of the scenario.                                                                                                         |
    | `gross_loss`        | _float_     | Gross loss of the scenario in USD.                                                                                                 |
    | `retro`             | _float_     | Retro for the scenario in USD.                                                                                                     |
    | `reinstatement`     | _float_     | Reinstatment for the scenario in USD.                                                                                              |
    | `timeline`          | _list_      | Timeline for the scenario's gross loss evolution.                                                                                  |

    """
    if not validate_uuid4(scenariolist_id):
        raise ValueError(f'{scenariolist_id} is not a valid UUID.')

    if not policies:
        raise ValueError('Policies are not provided.')

    if not isinstance(policies, list) or not all(isinstance(policy, int) for policy in policies):
        raise ValueError('Policies should be a list of integers.')

    if not computation_date:
        raise ValueError('Computation date is not provided.')

    try:
        datetime.strptime(computation_date, ISO_8601).date()
    except TypeError:
        raise ValueError('Computation date should be a string.')
    except ValueError:
        raise ValueError(f'{computation_date} is not a valid ISO 8601 date.')

    logger.info('Fetching aggregation from Allphins API.')

    return ScenarioList(scenariolist_id).aggregation(policies, computation_date).to_pandas()


def get_scenario_list_composition(
    scenariolist_id: uuid.UUID,
    computation_date: Optional[str] = datetime.now().strftime('%Y-%m-%d'),
) -> DataFrame:
    """Get layers composition for each scenario of a given scenariolist.

    Due to technical limitations, we currently prevent any query if there is more than 500k results.

    Args:
        scenariolist_id (uuid.UUID): UUID of the scenario list.
        computation_date (Optional[str]): Date of the computation, default to today.

    Returns:
        dataframe of the scenariolist's composition.

    ##### Response structure
    | Attribute           | Type        | Description                                                                                                                        |
    | ------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
    | `scenario_id`       | _int_       | Unique identifier for the scenario.                                                                                                |
    | `scenario_name`     | _string_    | Name of the scenario.                                                                                                              |
    | `cedant_name`       | _string_    | Name of the cedant.                                                                                                                |
    | `portfolio_name`    | _string_    | Name of the portfolio.                                                                                                             |
    | `policy_id`         | _int_       | Unique identifier for the policy.                                                                                                  |
    | `policy_name`       | _string_    | Name of the policy.                                                                                                                |
    | `client_loss`       | _float_     | Cedant loss of the layer in USD.                                                                                                   |
    | `gross_loss`        | _float_     | Gross loss of the layer in USD.                                                                                                    |
    | `policy_loss`       | _float_     | Policy loss.                                                                                                                       |

    """
    if not validate_uuid4(scenariolist_id):
        raise ValueError(f'{scenariolist_id} is not a valid UUID.')

    try:
        datetime.strptime(computation_date, ISO_8601).date()
    except TypeError:
        raise ValueError('Computation date should be a string.')
    except ValueError:
        raise ValueError(f'{computation_date} is not a valid ISO 8601 date.')

    logger.info('Fetching scenario list composition from Allphins API.')

    return ScenarioList(scenariolist_id).composition(computation_date).to_pandas()
