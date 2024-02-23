import pandas as pd


def cast_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to the correct data type."""
    data = df.copy()

    data["rain"] = data["rain"].astype("int32")
    data["temperature_2m"] = data["temperature_2m"].astype("int32")
    data["time"] = pd.to_datetime(data["time"])

    return data


def set_index(df: pd.DataFrame) -> pd.DataFrame:
    """Set the index of the DataFrame."""
    return df.set_index("time")


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns of the DataFrame."""
    data = df.copy()
    data.rename(columns={"temperature_2m": "temperature", "rain": "rainfall"})

    return data
