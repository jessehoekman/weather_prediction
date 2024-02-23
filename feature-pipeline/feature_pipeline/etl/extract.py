import datetime
from json import JSONDecodeError
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import requests
from yarl import URL

from feature_pipeline import utils

logger = utils.get_logger(__name__)


def from_api(
    days_delay: int = 5,
    days_export: int = 30,
    weather_variables: str = "temperature_2m,rain"
) -> Optional[Tuple[pd.DataFrame, Dict[str, Any]]]:
    """
    Args:
        days_delay: Data has a delay of N days. Thus, we have to shift our window with N days.
        days_export: The number of days to export.
        url: The URL of the API.
    Returns:
          A tuple of a Pandas DataFrame containing the exported data and a dictionary of metadata.
    """

    # Compute the export window.
    export_end = datetime.datetime.utcnow() - datetime.timedelta(days=days_delay)
    export_start = export_end - datetime.timedelta(days_export)

    # Define cities and their coordinates
    cities = {
        "Utrecht": {"latitude": "52.0908", "longitude": "5.1222"},
        "Amsterdam": {"latitude": "52.374", "longitude": "4.8897"},
    }

    # Placeholder for DataFrame collection
    dataframes = []

    # Iterate over cities to perform queries
    for city, coords in cities.items():

        url = "https://archive-api.open-meteo.com/v1/archive?"

        query_params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "start_date": export_start.strftime("%Y-%m-%d"),
            "end_date": export_end.strftime("%Y-%m-%d"),
            "hourly": weather_variables,
            "timezone": "Europe/London",
        }

        # Construct URL with query parameters
        url = URL(f"{url}latitude={query_params['latitude']}&longitude={query_params['longitude']}&start_date={query_params['start_date']}&end_date={query_params['end_date']}&hourly={query_params['hourly']}&timezone={query_params['timezone']}")
        logger.info(f"Requesting data from API for {city} with URL: {url}")

        # Make API request
        response = requests.get(url)
        logger.info(f"Response received from API for {city} with status code: {response.status_code}")

        # Parse API response
        try:
            response_data = response.json()
        except JSONDecodeError:
            logger.error(f"Response status = {response.status_code}. Could not decode response from API for {city} with URL: {url}")
            continue

        # Convert to DataFrame and add city column
        record = pd.DataFrame.from_records(response_data['hourly'])

        record['city'] = city
        record['coordinates'] = f"{coords['latitude']}, {coords['longitude']}"

        # Append DataFrame to list
        dataframes.append(record)

    # Combine all DataFrames
    records = pd.concat(dataframes, ignore_index=True)


    # Prepare metadata.
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    metadata = {
        "days_delay": days_delay,
        "days_export": days_export,
        "url": url,
        "export_datetime_utc_start": export_start.strftime(datetime_format),
        "export_datetime_utc_end": export_end.strftime(datetime_format),
        "datetime_format": datetime_format,
    }

    return records, metadata

from_api()