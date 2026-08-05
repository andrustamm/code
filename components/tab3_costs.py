import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import config


def render(df: pd.DataFrame):
    st.header("Kuu kulude graafik kategooriate kaupa")

    required_cols = [config.COL_PERIOD, config.COL_COST, config.COL_CATEGORY]
    if not df.empty and all(c in df.columns for c in required_cols):
        # 1. Group by PERIOOD and Category
        monthly_cat_df = (
            df.groupby([config.COL_PERIOD, config.COL_CATEGORY], dropna=False)[
                config.COL_COST
            ]
            .sum()
            .reset_index()
            .sort_values(by=config.COL_PERIOD)
        )

        # 2. Build stacked bar chart
        fig = px.bar(
            monthly_cat_df,
            x=config.COL_PERIOD,
            y=config.COL_COST,
            color=config.COL_CATEGORY,
            labels={
                config.COL_PERIOD: "Kuu",
                config.COL_COST: "Summa (€)",
                config.COL_CATEGORY: "Kategooria",
            },
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        # 3. Monthly totals for annotations
        totals_df = (
            monthly_cat_df.groupby(config.COL_PERIOD)[config.COL_COST]
            .sum()
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=totals_df[config.COL_PERIOD],
                y=totals_df[config.COL_COST],
                mode="text",
                text=totals_df[config.COL_COST].map("{:.2f} €".format),
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
            yaxis=dict(title="Summa (€)"),
            height=500,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Missing required columns for rendering cost chart.")