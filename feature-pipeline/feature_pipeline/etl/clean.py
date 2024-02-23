import pandas as pd


def cast_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to the correct data type."""
    data = df.copy()

    data["rain"] = data["rain"].astype("int32")
    data["temperature_2m"] = data["temperature_2m"].astype("int32")
    data["time"] = pd.to_datetime(data["time"])
    data["city"] = data["city"].astype("string").str.lower()

    return data

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns of the DataFrame."""
    data = df.copy()
    return data.rename(columns={"temperature_2m": "temperature", "rain": "rainfall"})

def sort_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Sort the columns of the DataFrame."""
    data = df.copy()
    return data[["city", "time", "temperature", "rainfall"]]


