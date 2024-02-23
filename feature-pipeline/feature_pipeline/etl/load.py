import hopsworks
import pandas as pd
from great_expectations.core import ExpectationSuite
from hsfs.feature_group import FeatureGroup

from feature_pipeline.settings import SETTINGS


def to_feature_store(
    data: pd.DataFrame,
    validation_expectation_suite: ExpectationSuite,
    feature_group_version: int = 1,
) -> FeatureGroup:
    """Function takes in a pandas DataFrame and a validation expectation suite,
    performs validation on the data using the suite, and then saves the data to a
    feature store in the feature store.
    """  # noqa: D205
    # Connect to feature store.
    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project="weather_prediction",
    )
    feature_store = project.get_feature_store()

    # Create feature group.
    weather_feature_group = feature_store.get_or_create_feature_group(
        name="weather_forecast",
        version=feature_group_version,
        description="Temperature and rain forecast for Utrecht, The Netherlands. Data is uploaded with a 5 days delay.",
        primary_key=["city"],
        event_time="time",
        online_enabled=False,
        expectation_suite=validation_expectation_suite,
    )
    # Upload data.
    weather_feature_group.insert(
        features=data,
        overwrite=False,
        write_options={
            "wait_for_job": True,
        },
    )

    # Add feature descriptions.
    feature_descriptions = [
        {
            "name": "time",
            "description": """
                            Datetime interval when the data was observed.
                            """,
            "validation_rules": "Always full hours, i.e. minutes are 00",
        },
        {
            "name": "temperature_2m",
            "description": "avg temperature in Celcius per hour.",
            "validation_rules": ">=-300 (int)",
        },
        {
            "name": "rain",
            "description": "Total rainfall in millimeters per hour.",
            "validation_rules": ">=0 (int)",
        },
    ]
    for description in feature_descriptions:
        weather_feature_group.update_feature_description(
            description["name"], description["description"]
        )

    # Update statistics.
    weather_feature_group.statistics_config = {
        "enabled": True,
        "histograms": True,
        "correlations": True,
    }
    weather_feature_group.update_statistics_config()
    weather_feature_group.compute_statistics()

    return weather_feature_group
