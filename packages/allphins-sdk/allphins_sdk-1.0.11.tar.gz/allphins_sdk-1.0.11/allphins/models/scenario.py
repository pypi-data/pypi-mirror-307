"""Scenario model.

```
from allphins.models import Scenario
```
"""

from allphins.const import ALLPHINS_API_URL
from allphins.models.base import BaseModel


class Scenario(BaseModel):
    """Scenario model."""

    path = f'{ALLPHINS_API_URL}/scenarios/'
