import logging
from typing import List, Dict, Any
from datetime import datetime
from statforge.utils.http import fetch_json

logger = logging.getLogger(__name__)

STATSCAN_API_URL = "https://www150.statcan.gc.ca/t1/wds/rest"

def get_series_info(vector_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieves metadata for a list of StatCan vector IDs.
    Endpoint: /getSeriesInfoFromVector
    """
    url = f"{STATSCAN_API_URL}/getSeriesInfoFromVector"
    payload = [{"vectorId": v} for v in vector_ids]
    
    data = fetch_json(url, method="POST", json_body=payload)
    
    # StatCan returns a list of objects, some might be errors.
    # Structure: [{"status": "SUCCESS", "object": {...}}, ...]
    results = []
    for item in data:
        if item.get("status") == "SUCCESS":
            results.append(item["object"])
        else:
            logger.warning(f"Failed to fetch info for vector: {item}")
            
    return results

def get_data_from_vectors(vector_ids: List[str], start_date: datetime = None) -> List[Dict[str, Any]]:
    """
    Retrieves data points for a list of StatCan vector IDs.
    Endpoint: /getDataFromVectorsAndLatestNPeriods 
    (or similar, depending on need. Using getDataFromVectorsAndLatestNPeriods for now or a range).
    
    Actually, to get a specific range, we use:
    /getDataFromVectorsAndLatestNPeriods (if we want last N)
    OR
    /getDataFromVectorByReferencePeriodRange
    """
    
    # For bulk history, ReferencePeriodRange is better.
    # If start_date is None, default to a wide range or last 10 years? 
    # Let's use a safe default of "2000-01-01" if not provided.
    
    start_str = start_date.strftime("%Y-%m-%d") if start_date else "2000-01-01"
    # End date open-ended (StatCan usually takes '2099-12-31' or similar for 'now')
    end_str = "2099-12-31"

    url = f"{STATSCAN_API_URL}/getDataFromVectorByReferencePeriodRange"
    payload = []
    for v in vector_ids:
        payload.append({
            "vectorId": v,
            "startReferencePeriod": start_str,
            "endReferencePeriod": end_str
        })

    data = fetch_json(url, method="POST", json_body=payload)
    
    results = []
    for item in data:
        if item.get("status") == "SUCCESS":
            results.append(item["object"])
        else:
            logger.warning(f"Failed to fetch data for vector: {item}")
    
    return results
