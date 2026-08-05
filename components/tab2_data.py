import pandas as pd
import streamlit as st
import config


def render(df: pd.DataFrame):
    st.header("Andmed")
    if df.empty:
        st.warning("No CSV files found in the `/data` folder.")
    else:
        valid_cols = [c for c in config.DISPLAY_COLUMNS if c in df.columns]
        st.dataframe(
            df[valid_cols] if valid_cols else df,
            use_container_width=True,
        )