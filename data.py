import ast
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str = "Dataset/Tweets.csv") -> pd.DataFrame:
    """Load and basic-process the tweets dataset.

    Caches the result using Streamlit so repeated runs are fast.
    """
    data = pd.read_csv(path)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"]) 
    return data


def map_plot_data(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of rows with coordinates expanded into `latitude` and `longitude`.

    The original `tweet_coord` column can be a stringified list or NA.
    """
    df = data[data["tweet_coord"].notna()].copy()

    def _extract_coords(x):
        if isinstance(x, str):
            try:
                vals = ast.literal_eval(x)
            except Exception:
                return pd.Series([None, None])
            return pd.Series(vals).reindex([0, 1])
        else:
            return pd.Series(x).reindex([0, 1])

    df[["latitude", "longitude"]] = df["tweet_coord"].apply(lambda x: _extract_coords(x))
    return df
