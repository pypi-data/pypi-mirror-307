"""Constants for the project."""
import os
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

ALLPHINS_API_URL = f"{os.environ.get('ALLPHINS_URL', 'https://api.allphins.com')}/api/v1"
ACCESS_TOKEN_URL = f'{ALLPHINS_API_URL}/token/'
REFRESH_TOKEN_URL = f'{ALLPHINS_API_URL}/token/refresh/'
SSL_IGNORE = os.environ.get('SSL_IGNORE', 'False').lower() in ('true', '1', 'yes')

try:
    USER_AGENT = f'Allphins SDK/{version("allphins-sdk")}'
except PackageNotFoundError:
    USER_AGENT = 'Allphins SDK/default'

GET = 'GET'
POST = 'POST'

ISO_8601 = '%Y-%m-%d'
