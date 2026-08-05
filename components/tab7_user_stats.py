# components/tab7_user_stats.py
import pandas as pd
import streamlit as st
import config
from utils.formatters import format_bytes, format_minutes_to_hm


def render(df: pd.DataFrame):
    st.header("Kasutajate statistika üldülevaade")

    if df.empty or config.COL_NUMBER not in df.columns:
        st.info("Andmed puuduvad või puudub vajalik tulp 'SIDEVAHEND'.")
        return

    valid_df = df[df[config.COL_NUMBER].notna() & (df[config.COL_NUMBER] != "")].copy()

    if valid_df.empty:
        st.info("Sidevahendite kohta andmed puuduvad.")
        return

    # Count unique months in the currently filtered dataset
    num_months = (
        valid_df[config.COL_PERIOD].nunique()
        if config.COL_PERIOD in valid_df.columns
        else 0
    )
    month_label = "kuu" if num_months == 1 else "kuu"

    # 1. Base Column Conversions
    valid_df["COST_VAL"] = pd.to_numeric(valid_df[config.COL_COST], errors="coerce").fillna(0)

    # Call Minutes
    calls_mask = valid_df[config.COL_CATEGORY] == "Kõned"
    valid_df["CALL_MINS"] = 0.0
    if config.COL_MINUTES in valid_df.columns:
        valid_df.loc[calls_mask, "CALL_MINS"] = pd.to_numeric(
            valid_df.loc[calls_mask, config.COL_MINUTES], errors="coerce"
        ).fillna(0)

    # Data GB
    valid_df["DATA_GB"] = 0.0
    if config.COL_DATA in valid_df.columns:
        valid_df["DATA_GB"] = pd.to_numeric(
            valid_df[config.COL_DATA], errors="coerce"
        ).fillna(0)

    # SMS Count
    sms_mask = valid_df[config.COL_CATEGORY] == "Sõnumid"
    count_col = config.COL_COUNT if config.COL_COUNT in valid_df.columns else "SMS_COUNT"
    if count_col not in valid_df.columns:
        valid_df["SMS_COUNT"] = 1
        count_col = "SMS_COUNT"
    valid_df["SMS_QTY"] = 0
    valid_df.loc[sms_mask, "SMS_QTY"] = pd.to_numeric(
        valid_df.loc[sms_mask, count_col], errors="coerce"
    ).fillna(1).astype(int)

    # Parking Cost
    parking_mask = valid_df[config.COL_CATEGORY] == "Parkimine"
    if config.COL_RAW_SERVICE in valid_df.columns:
        parking_mask = parking_mask | valid_df[config.COL_RAW_SERVICE].astype(str).str.contains("park", case=False, na=False)
    
    valid_df["PARKING_COST"] = 0.0
    valid_df.loc[parking_mask, "PARKING_COST"] = valid_df.loc[parking_mask, "COST_VAL"]

    # -------------------------------------------------------------
    # Step A: Aggregate by Number AND Month (To compute monthly medians)
    # -------------------------------------------------------------
    monthly_per_user = valid_df.groupby([config.COL_NUMBER, config.COL_PERIOD]).agg(
        MONTHLY_COST=("COST_VAL", "sum"),
        MONTHLY_MINS=("CALL_MINS", "sum"),
        MONTHLY_DATA=("DATA_GB", "sum"),
        MONTHLY_SMS=("SMS_QTY", "sum"),
        MONTHLY_PARK=("PARKING_COST", "sum"),
    ).reset_index()

    medians = monthly_per_user.groupby(config.COL_NUMBER).agg(
        MEDIAN_COST=("MONTHLY_COST", "median"),
        MEDIAN_MINS=("MONTHLY_MINS", "median"),
        MEDIAN_DATA=("MONTHLY_DATA", "median"),
        MEDIAN_SMS=("MONTHLY_SMS", "median"),
        MEDIAN_PARK=("MONTHLY_PARK", "median"),
    ).reset_index()

    # -------------------------------------------------------------
    # Step B: Aggregate Totals Across Whole Period
    # -------------------------------------------------------------
    totals = valid_df.groupby(config.COL_NUMBER).agg(
        TOTAL_COST=("COST_VAL", "sum"),
        TOTAL_CALL_MINS=("CALL_MINS", "sum"),
        TOTAL_DATA_GB=("DATA_GB", "sum"),
        TOTAL_SMS=("SMS_QTY", "sum"),
        TOTAL_PARKING_COST=("PARKING_COST", "sum"),
    ).reset_index()

    # Merge Totals and Medians
    stats = pd.merge(totals, medians, on=config.COL_NUMBER)

    # Dynamic subheader title for KPI Cards
    st.subheader(f"Üldised näitajad ({num_months} {month_label} andmed)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Kõneaeg kokku", format_minutes_to_hm(stats["TOTAL_CALL_MINS"].sum()))
    m2.metric("Andmeside kokku", format_bytes(stats["TOTAL_DATA_GB"].sum()))
    m3.metric("Sõnumid kokku", f"{stats['TOTAL_SMS'].sum()} tk")
    m4.metric("Parkimine kokku", f"{stats['TOTAL_PARKING_COST'].sum():.2f} €")

    st.markdown("---")

    # -------------------------------------------------------------
    # Step C: Construct Grouped Header MultiIndex DataFrame
    # -------------------------------------------------------------
    grouped_df = pd.DataFrame()

    # Main index column
    grouped_df[("", "Sidevahend")] = stats[config.COL_NUMBER]

    # Major Group 1: Kokku (Total)
    grouped_df[("Kokku", "Andmemaht")] = stats["TOTAL_DATA_GB"].apply(format_bytes)
    grouped_df[("Kokku", "Kõnekestus")] = stats["TOTAL_CALL_MINS"].apply(format_minutes_to_hm)
    grouped_df[("Kokku", "Sõnumid")] = stats["TOTAL_SMS"].astype(int).astype(str) + " tk"
    grouped_df[("Kokku", "Parkimine")] = stats["TOTAL_PARKING_COST"].round(2).apply(lambda x: f"{x:.2f} €")
    grouped_df[("Kokku", "Kogukulu")] = stats["TOTAL_COST"].round(2).apply(lambda x: f"{x:.2f} €")

    # Major Group 2: Mediaan (kuu) (Monthly Median)
    grouped_df[("Mediaan (kuu)", "Andmemaht")] = stats["MEDIAN_DATA"].apply(format_bytes)
    grouped_df[("Mediaan (kuu)", "Kõnekestus")] = stats["MEDIAN_MINS"].apply(format_minutes_to_hm)
    grouped_df[("Mediaan (kuu)", "Sõnumid")] = stats["MEDIAN_SMS"].round(1).astype(str) + " tk"
    grouped_df[("Mediaan (kuu)", "Parkimine")] = stats["MEDIAN_PARK"].round(2).apply(lambda x: f"{x:.2f} €")
    grouped_df[("Mediaan (kuu)", "Kogukulu")] = stats["MEDIAN_COST"].round(2).apply(lambda x: f"{x:.2f} €")

    # Convert columns to MultiIndex
    grouped_df.columns = pd.MultiIndex.from_tuples(grouped_df.columns)

    # Style right alignment for cell values and headers
    styled_df = (
        grouped_df.style.set_properties(**{"text-align": "right"})
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "right")]},
            {"selector": "td", "props": [("text-align", "right")]},
        ])
    )

    # Dynamic subheader title for Table
    st.subheader(f"Sidevahendite kaupa statistika ({num_months} {month_label} andmed)")
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
    )