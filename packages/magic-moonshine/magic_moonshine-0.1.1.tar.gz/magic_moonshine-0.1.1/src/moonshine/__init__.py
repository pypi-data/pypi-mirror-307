import os
import json
import urllib.parse
import requests
from typing import Dict, Optional

_CONFIG = {
    'api_token': None
}

def config(API: str) -> None:
    """
    Configure the Moonshine client with your API token.
    
    Args:
        API (str): Your Moonshine API token
    """
    _CONFIG['api_token'] = API

def search(bucket: str, query: str) -> Dict:
    """
    Search media using the Moonshine API.
    
    Args:
        bucket (str): The project/bucket ID to search in
        query (str): The search query
    
    Returns:
        Dict: The API response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/media-query"
    
    params = {
        'projectid': bucket,
        'api': _CONFIG['api_token'],
        'query': query,
        'numargs': 5,
        'threshold': 15
    }
    
    # Construct URL with properly encoded parameters
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")