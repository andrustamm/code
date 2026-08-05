import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import config


def render(df: pd.DataFrame):
    st.header("Andmeside kuupõhine graafik sidevahendite kaupa")

    required_cols = [config.COL_PERIOD, config.COL_DATA, config.COL_NUMBER]
    if not df.empty and all(c in df.columns for c in required_cols):
        # Filter for 'Kõned' category
        data_df = df[df[config.COL_CATEGORY] == "Mobiilne internet"]

        if data_df.empty:
            st.info("Kategoorias 'Mobiilne internet' andmed puuduvad.")
            return


    if not data_df.empty and all(c in data_df.columns for c in required_cols):
        # 1. Group by PERIOOD and SIDEVAHEND
        monthly_number_df = (
            data_df.groupby([config.COL_PERIOD, config.COL_NUMBER], dropna=False)[
                config.COL_DATA
            ]
            .sum()
            .reset_index()
            .sort_values(by=config.COL_PERIOD)
        )

        # 2. Build stacked bar chart
        fig = px.bar(
            monthly_number_df,
            x=config.COL_PERIOD,
            y=config.COL_DATA,
            color=config.COL_NUMBER,
            labels={
                config.COL_PERIOD: "Kuu",
                config.COL_DATA: "Andmemaht (GB)",
                config.COL_NUMBER: "Sidevahend",
            },
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        # 3. Calculate totals for bar labels
        totals_df = (
            monthly_number_df.groupby(config.COL_PERIOD)[config.COL_DATA]
            .sum()
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=totals_df[config.COL_PERIOD],
                y=totals_df[config.COL_DATA],
                mode="text",
                text=totals_df[config.COL_DATA].map("{:.2f} GB".format),
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
            yaxis=dict(title="Andmemaht (GB)"),
            legend_title_text="Sidevahend",
            height=500,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Missing required columns for data usage charting.")