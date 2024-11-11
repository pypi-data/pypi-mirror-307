import requests
import time
import os
from cybertek_api import log_request_to_db

REQUEST_LOG_URL = os.getenv('REQUEST_LOG_URL')

def get_assets_all(api_baseurl, api_key):
    """
    Retrieve assets from the API across all customers.

    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of all assets.

    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """

    url = f'{api_baseurl}/customer_assets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_assets = []
    page = 1

    while True:
        params = {"page": page}
        try:
            response = requests.get(url, headers=headers, params=params)
            log_request_to_db(REQUEST_LOG_URL, "get_assets_all", url, 222)
            response.raise_for_status()
            data = response.json()
            all_assets.extend(data["assets"])
            meta = data.get('meta', {})
            total_pages = meta.get('total_pages', 1)
            
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch assets on page {page}: {str(e)}")
        
    return all_assets
