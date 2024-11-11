import requests
import logging
import time
import os
#from cybertek_api import log_request_to_db

REQUEST_LOG_URL = os.getenv('REQUEST_LOG_URL')

# Set up logging for the module
logger = logging.getLogger(__name__)

def get_customers_managed(api_baseurl, api_key):
    """
    Retrieve a list of managed customers from the API with pagination.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
    
    Returns:
        list: A list of managed customers.
    
    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """
    if not api_baseurl:
        raise ValueError("API base URL must be provided.")
    if not api_key:
        raise ValueError("API key must be provided.")
    
    url = f'{api_baseurl}/customers'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    
    managed_customers = []
    page = 1
    
    while True:
        try:
            response = requests.get(f'{url}?page={page}', headers=headers)
            #log_request_to_db(REQUEST_LOG_URL, "get_customers_managed", url, 222)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            # Safely get customers and meta data
            customers_data = response.json().get('customers', [])
            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)

            # Filter customers based on "Managed Status"
            for customer in customers_data:
                if 'properties' in customer and customer['properties'].get("Managed Status") == 35984:
                    managed_customers.append(customer)

            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(2)

        except requests.exceptions.RequestException as ex:
            logger.error(f"An error occurred while fetching managed customers: {ex}")
            break  # Exit the loop on error
    
    return managed_customers


def get_customers_all(api_baseurl, api_key):
    """
    Retrieve a list of customers from the API with pagination.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
    
    Returns:
        list: A list of customers.
    
    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """
    if not api_baseurl:
        raise ValueError("API base URL must be provided.")
    if not api_key:
        raise ValueError("API key must be provided.")
    
    url = f'{api_baseurl}/customers?include_disabled=true'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    all_syncro_customers = []
    page = 1
    
    while True:
        try:
            response = requests.get(f'{url}?page={page}', headers=headers)
            #log_request_to_db(REQUEST_LOG_URL, "get_customers_all", url, 222)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Safely get customers and meta data
            customers_data = response.json().get('customers', [])
            all_syncro_customers.extend(customers_data)
            
            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(2)

        except requests.exceptions.RequestException as ex:
            logging.error(f"An error occurred while fetching customers: {ex}")
            break  # Exit the loop on error
    
    return all_syncro_customers
