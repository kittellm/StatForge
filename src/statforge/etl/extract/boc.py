import logging
from typing import Dict, Any, Optional
from statforge.utils.http import fetch_json

logger = logging.getLogger(__name__)

BOC_API_URL = "https://www.bankofcanada.ca/valet"

def get_series_observations(series_name: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """
    Fetches observations for a specific Bank of Canada series.
    Example series: 'FXUSDCAD' (US to CAD exchange rate)
    """
    url = f"{BOC_API_URL}/observations/{series_name}/json"
    
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
        
    data = fetch_json(url, params=params)
    return data

def get_series_details(series_name: str) -> Dict[str, Any]:
    """
    Fetches metadata/details for a specific Bank of Canada series.
    """
    url = f"{BOC_API_URL}/series/{series_name}/json"
    data = fetch_json(url)
    return data
