import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import config
from utils.formatters import format_minutes_to_hm


def render(df: pd.DataFrame):
    st.header("Kõneminutid kuus sidevahendite kaupa")

    required_cols = [
        config.COL_PERIOD,
        config.COL_MINUTES,
        config.COL_NUMBER,
        config.COL_CATEGORY,
    ]
    if not df.empty and all(c in df.columns for c in required_cols):
        # Filter for 'Kõned' category
        calls_df = df[df[config.COL_CATEGORY] == "Kõned"]

        if calls_df.empty:
            st.info("Kategoorias 'Kõned' andmed puuduvad.")
            return

        # 1. Group by PERIOOD and SIDEVAHEND
        monthly_calls_df = (
            calls_df.groupby([config.COL_PERIOD, config.COL_NUMBER], dropna=False)[
                config.COL_MINUTES
            ]
            .sum()
            .reset_index()
            .sort_values(by=config.COL_PERIOD)
        )

        # Pre-compute formatted string for hover tooltips
        monthly_calls_df["KESTUS_HM"] = monthly_calls_df[
            config.COL_MINUTES
        ].apply(format_minutes_to_hm)

        # 2. Build stacked bar chart
        fig = px.bar(
            monthly_calls_df,
            x=config.COL_PERIOD,
            y=config.COL_MINUTES,
            color=config.COL_NUMBER,
            custom_data=["KESTUS_HM"],
            labels={
                config.COL_PERIOD: "Kuu",
                config.COL_MINUTES: "Kõnekestus (min)",
                config.COL_NUMBER: "Sidevahend",
            },
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        fig.update_traces(
            hovertemplate="<b>Sidevahend: %{fullData.name}</b><br>Kuu: %{x}<br>Kestus: %{customdata[0]}<extra></extra>"
        )

        # 3. Total text labels formatted as xxH yyM
        totals_df = (
            monthly_calls_df.groupby(config.COL_PERIOD)[config.COL_MINUTES]
            .sum()
            .reset_index()
        )
        totals_df["TOTAL_HM"] = totals_df[config.COL_MINUTES].apply(
            format_minutes_to_hm
        )

        fig.add_trace(
            go.Scatter(
                x=totals_df[config.COL_PERIOD],
                y=totals_df[config.COL_MINUTES],
                mode="text",
                text=totals_df["TOTAL_HM"],
                textposition="top center",
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # 4. Polish layout
        fig.update_layout(
            barmode="stack",
            xaxis_type="category",
            xaxis=dict(title="Kuu"),
            yaxis=dict(title="Kõnekestus (minutid)"),
            legend_title_text="Sidevahend",
            height=500,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Missing required columns for call duration charting.")