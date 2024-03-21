import pandas as pd

from feature_pipeline import utils
from feature_pipeline.etl import clean, extract, load, validation

logger = utils.get_logger(__name__)


def run(
    feature_group_version: int = 2,
) -> dict:
    """Extract data from the API.

    Args:
    ----
        export_end_reference_datetime: The end reference datetime of the export window. If None, the current time is used.
            Because the data is always delayed with "days_delay" days, this date is used only as a reference point.
            The real extracted window will be computed as [export_end_reference_datetime - days_delay - days_export, export_end_reference_datetime - days_delay].
        days_delay: Data has a delay of N days. Thus, we have to shift our window with N days.
        days_export: The number of days to export.
        url: The URL of the API.
        feature_group_version: The version of the feature store feature group to save the data to.

    Returns:
    -------
          A dictionary containing metadata of the pipeline.

    """
    logger.info("Extracting data from OpenMeteo API.")
    data, metadata = extract.from_api()
    logger.info("Successfully extracted data from OpenMeteo API.")

    logger.info("Cleaning data.")
    data = transform(data)
    logger.info("Successfully cleaned data.")

    logger.info("Building validation expectation suite.")
    validation_expectation_suite = validation.build_expectation_suite()
    logger.info("Successfully built validation expectation suite.")

    logger.info("Validating data and loading it to the feature store.")
    load.to_feature_store(
        data,
        validation_expectation_suite=validation_expectation_suite,
        feature_group_version=feature_group_version,
    )
    metadata["feature_group_version"] = feature_group_version
    logger.info("Successfully validated data and loaded it to the feature store.")

    logger.info("Wrapping up the pipeline.")
    utils.save_json(metadata, file_name="feature_pipeline_metadata.json")
    logger.info("Done!")

    return metadata


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper containing all the transformations from the ETL pipeline."""
    data = df.copy()
    data = clean.cast_columns(data)
    data = clean.rename_columns(data)
    return clean.sort_columns(data)


run()
