# app.py
import pandas as pd
import streamlit as st
from components import tab8_category_rules

import config
from utils import get_folder_state, load_and_combine_csvs
from components import (
    render_tab1,
    render_tab2,
    render_tab3,
    render_tab4,
    render_tab5,
    render_tab6,
    render_tab7,
    render_tab8,
)

# Set page config
st.set_page_config(page_title="Sidekulude andmed", layout="wide")

# Header with refresh button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Sidekulude andmed")
with col2:
    if st.button("🔄 Värskenda andmed"):
        st.cache_data.clear()
        st.rerun()

# Load Data dynamically
folder_state = get_folder_state(config.DATA_DIR)
df_raw = load_and_combine_csvs(config.DATA_DIR, folder_state)

# --- GLOBAL SIDEBAR FILTERS ---
df = df_raw.copy()

if not df_raw.empty:
    st.sidebar.header("🔍 Filtrid")

    # 1. Period Filter
    if config.COL_PERIOD in df_raw.columns:
        available_periods = sorted(
            [p for p in df_raw[config.COL_PERIOD].unique() if p != "Teadmata"]
        )
        if available_periods:
            selected_periods = st.sidebar.multiselect(
                "Vali periood (YYYY-MM):",
                options=available_periods,
                default=available_periods,
            )
            df = df[df[config.COL_PERIOD].isin(selected_periods)]

    # 2. Phone Number Filter
    if config.COL_NUMBER in df_raw.columns:
        available_numbers = sorted(
            [str(n) for n in df_raw[config.COL_NUMBER].unique() if pd.notna(n)]
        )
        if available_numbers:
            selected_numbers = st.sidebar.multiselect(
                "Vali sidevahend:",
                options=available_numbers,
                default=available_numbers,
            )
            df = df[df[config.COL_NUMBER].isin(selected_numbers)]

# Render 7 Tabs using the filtered DataFrame `df`
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Selgitused",
        "Andmed",
        "Kuu kulude graafik",
        "Andmeside kuupõhine graafik",
        "Kõneminutid kuus",
        "Sõnumid kuus",
        "Kasutaja statistika",
        "Kategooriate haldus",
    ]
)

with tab1:
    render_tab1()

with tab2:
    render_tab2(df)

with tab3:
    render_tab3(df)

with tab4:
    render_tab4(df)

with tab5:
    render_tab5(df)

with tab6:
    render_tab6(df)

with tab7:
    render_tab7(df)

with tab8:
    render_tab8()