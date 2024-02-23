logger = utils.get_logger(__name__)


def run(
    export_end_reference_datetime: Optional[datetime.datetime] = None,
    days_delay: int = 5,
    days_export: int = 30,
    url: str = "https://archive-api.open-meteo.com/v1/archive",
    feature_group_version: int = 1,
) -> dict:
    """
    Extract data from the API.
    Args:
        export_end_reference_datetime: The end reference datetime of the export window. If None, the current time is used.
            Because the data is always delayed with "days_delay" days, this date is used only as a reference point.
            The real extracted window will be computed as [export_end_reference_datetime - days_delay - days_export, export_end_reference_datetime - days_delay].
        days_delay: Data has a delay of N days. Thus, we have to shift our window with N days.
        days_export: The number of days to export.
        url: The URL of the API.
        feature_group_version: The version of the feature store feature group to save the data to.
    Returns:
          A dictionary containing metadata of the pipeline.
    """

    logger.info(f"Extracting data from API.")
    data, metadata = extract.from_api(
        export_end_reference_datetime, days_delay, days_export, url
    )
    logger.info("Successfully extracted data from API.")

    logger.info(f"Transforming data.")
    data = transform(data)
    logger.info("Successfully transformed data.")

    logger.info("Building validation expectation suite.")
    validation_expectation_suite = validation.build_expectation_suite()
    logger.info("Successfully built validation expectation suite.")

    logger.info(f"Validating data and loading it to the feature store.")
    load.to_feature_store(
        data,
        validation_expectation_suite=validation_expectation_suite,
        feature_group_version=feature_group_version,
    )
    metadata["feature_group_version"] = feature_group_version
    logger.info("Successfully validated data and loaded it to the feature store.")

    logger.info(f"Wrapping up the pipeline.")
    utils.save_json(metadata, file_name="feature_pipeline_metadata.json")
    logger.info("Done!")

    return metadata