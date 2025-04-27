import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def make_request(method, url, data=None, headers=None, timeout=30):
    """
    Make HTTP request to mPAY ONE API
    
    Args:
        method (str): HTTP method (GET, POST, PUT, DELETE)
        url (str): Request URL
        data (dict, optional): Request payload
        headers (dict, optional): Request headers
        timeout (int, optional): Request timeout in seconds
        
    Returns:
        requests.Response: Response object
    
    Raises:
        RequestException: If request fails
    """
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    try:
        logger.debug(f"Making {method} request to {url}")
        if data:
            logger.debug(f"Request payload: {data}")
        
        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=headers,
            timeout=timeout
        )
        
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        
        # Raise exception for 4XX/5XX responses
        response.raise_for_status()
        
        return response
    
    except RequestException as e:
        logger.error(f"HTTP request failed: {str(e)}")
        
        # Return the response even if status code indicates error
        if hasattr(e, 'response') and e.response is not None:
            return e.response
        
        # Re-raise the exception if no response
        raise
