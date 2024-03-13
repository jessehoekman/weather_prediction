import logging

import fire
import hopsworks

from feature_pipeline import settings


def clean() -> None:
    """Utility function used during development to clean all the data from the feature store."""
    project = hopsworks.login(
        api_key_value=settings.SETTINGS["FS_API_KEY"],
        project=settings.SETTINGS["FS_PROJECT_NAME"],
    )
    fs = project.get_feature_store()

    logging.info("Deleting feature views and training datasets...")
    try:
        feature_views = fs.get_feature_views(name="weather_prediction")

        for feature_view in feature_views:
            feature_view.delete()
    except Exception:
        logging.exception("Found an error")

    logging.info("Deleting feature groups...")
    try:
        feature_groups = fs.get_feature_groups(name="weather_prediction")
        for feature_group in feature_groups:
            feature_group.delete()
    except Exception:
        logging.exception("Found an error")


if __name__ == "__main__":
    fire.Fire(clean)
