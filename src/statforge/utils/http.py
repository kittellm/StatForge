import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)

def get_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    Creates or configures a requests Session with automatic retries.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_json(url: str, params: dict = None, method: str = "GET", json_body: dict = None) -> dict:
    """
    Helper to fetch JSON from a URL with retries.
    """
    session = get_retry_session()
    try:
        if method.upper() == "GET":
            response = session.get(url, params=params, timeout=10)
        elif method.upper() == "POST":
            response = session.post(url, json=json_body, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        raise
