from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

import config
from .formatters import format_period_string, parse_duration_to_minutes


def get_folder_state(data_folder: Path) -> tuple:
    """Generates a cache key based on file modification times."""
    if not data_folder.exists():
        return ()
    return tuple(
        (f.name, f.stat().st_mtime) for f in sorted(data_folder.glob("*.csv"))
    )


@st.cache_data
def load_and_combine_csvs(
    data_folder: Path, folder_state: tuple
) -> pd.DataFrame:
    """Finds all CSV files in data directory and combines them into one DataFrame."""
    if not data_folder.exists() or not data_folder.is_dir():
        return pd.DataFrame()

    csv_files = list(data_folder.glob("*.csv"))
    if not csv_files:
        return pd.DataFrame()

    dataframes = [pd.read_csv(file, sep=";", decimal=",") for file in csv_files]
    df = pd.concat(dataframes, ignore_index=True)

    if df.empty:
        return df

    # 1. Transform 'PERIOOD' safely to '%Y-%m' string
    if config.COL_PERIOD in df.columns:
        df[config.COL_PERIOD] = df[config.COL_PERIOD].apply(format_period_string)

    # 2. Add Category based on 'TEENUSED'
    if config.COL_RAW_SERVICE in df.columns:
        service_series = df[config.COL_RAW_SERVICE].astype(str).str.lower()
        conditions = [
            service_series.str.contains(pat, na=False)
            for pat, _ in config.CATEGORY_RULES
        ]
        choices = [label for _, label in config.CATEGORY_RULES]
        df[config.COL_CATEGORY] = np.select(conditions, choices, default="Muu")
    else:
        df[config.COL_CATEGORY] = "Muu"

    # 3. Clean numeric columns
    if config.COL_COST in df.columns:
        df[config.COL_COST] = pd.to_numeric(
            df[config.COL_COST], errors="coerce"
        ).fillna(0)

    if config.COL_DATA in df.columns:
        # Convert raw KB values to GB (divide by 1024 * 1024)
        df[config.COL_DATA] = (
            pd.to_numeric(df[config.COL_DATA], errors="coerce").fillna(0)
            / (1024 * 1024)
        )

    if config.COL_DURATION in df.columns:
        df[config.COL_MINUTES] = df[config.COL_DURATION].apply(
            parse_duration_to_minutes
        )
    else:
        df[config.COL_MINUTES] = 0.0

    if config.COL_NUMBER in df.columns:
        df[config.COL_NUMBER] = df[config.COL_NUMBER].fillna("Teadmata").astype(str)

    return df