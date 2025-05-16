# data_fetcher.py
"""
Module responsible for fetching animal data from various sources.
Provides a unified interface to retrieve data regardless of implementation.
"""

import os
from urllib.parse import urlsplit, urlunsplit

import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
_RAW_URL = os.getenv('API_URL', 'https://api.api-ninjas.com/v1/animals')
_split = urlsplit(_RAW_URL)
API_URL = urlunsplit((_split.scheme, _split.netloc, _split.path, '', ''))
HEADERS = {'X-Api-Key': API_KEY} if API_KEY else {}


def fetch_data(animal_name):
    """
    Fetches the animals data for the given 'animal_name' from the API.

    Returns:
        list of dicts, each dict has:
        {
            'name': str,
            'taxonomy': dict,
            'locations': list[str],
            'characteristics': dict
        }
    """
    if not API_KEY:
        raise RuntimeError('API_KEY is not defined in .env')

    params = {'name': animal_name}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise RuntimeError(f'HTTP error: {err}. Response: {response.text}')

    data = response.json()
    # Normalize to list
    return data if isinstance(data, list) else [data]

