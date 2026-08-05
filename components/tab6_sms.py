import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import config


def render(df: pd.DataFrame):
    st.header("Sõnumite arv kuus sidevahendite kaupa")

    required_cols = [
        config.COL_PERIOD,
        config.COL_NUMBER,
        config.COL_CATEGORY,
    ]
    
    if not df.empty and all(c in df.columns for c in required_cols):
        # Filter strictly for 'Sõnumid' category
        sms_df = df[df[config.COL_CATEGORY] == "Sõnumid"].copy()

        if sms_df.empty:
            st.info("Kategoorias 'Sõnumid' andmed puuduvad.")
            return

        # Determine count column: use COL_COUNT ('KOGUS') if available, otherwise count rows
        count_col = config.COL_COUNT if config.COL_COUNT in sms_df.columns else "SMS_COUNT"
        if count_col == "SMS_COUNT":
            sms_df["SMS_COUNT"] = 1

        # 1. Group by PERIOOD and SIDEVAHEND
        monthly_sms_df = (
            sms_df.groupby([config.COL_PERIOD, config.COL_NUMBER], dropna=False)[count_col]
            .sum()
            .reset_index()
            .sort_values(by=config.COL_PERIOD)
        )

        # 2. Build stacked bar chart
        fig = px.bar(
            monthly_sms_df,
            x=config.COL_PERIOD,
            y=count_col,
            color=config.COL_NUMBER,
            labels={
                config.COL_PERIOD: "Kuu",
                count_col: "Sõnumite arv (tk)",
                config.COL_NUMBER: "Sidevahend",
            },
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        # 3. Calculate totals for bar top labels
        totals_df = (
            monthly_sms_df.groupby(config.COL_PERIOD)[count_col]
            .sum()
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=totals_df[config.COL_PERIOD],
                y=totals_df[count_col],
                mode="text",
                text=totals_df[count_col].astype(int).astype(str) + " tk",
                textposition="top center",
                textfont=dict(size=13, color="black"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # 4. Apply layout & font customization
        fig.update_layout(
            font=dict(size=13),
            barmode="stack",
            xaxis_type="category",
            xaxis=dict(
                title=dict(text="Kuu", font=dict(size=15)),
                tickfont=dict(size=12),
            ),
            yaxis=dict(
                title=dict(text="Sõnumite arv (tk)", font=dict(size=15)),
                tickfont=dict(size=12),
            ),
            legend=dict(
                title=dict(text="Sidevahend", font=dict(size=14)),
                font=dict(size=12),
            ),
            height=500,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Missing required columns for SMS charting.")