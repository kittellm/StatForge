import logging
import pandas as pd
from io import StringIO
import requests
from statforge.utils.http import get_retry_session

logger = logging.getLogger(__name__)

def download_csv(url: str) -> pd.DataFrame:
    """
    Downloads a CSV file from a URL and returns it as a pandas DataFrame.
    CMHC data is often available via direct CSV links from their portal.
    """
    session = get_retry_session()
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        # Use StringIO to read the string content as a file
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading CSV from {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error parsing CSV from {url}: {e}")
        raise
