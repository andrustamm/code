# utils/charts.py
import plotly.express as px
import plotly.graph_objects as go

def build_stacked_bar_chart(
    df, x_col, y_col, color_col, y_label, total_format_fn
):
    """Generic builder for stacked bar charts with total labels."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        labels={x_col: "Kuu", y_col: y_label, color_col: "Sidevahend"},
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    
    # Calculate totals per month
    totals = df.groupby(x_col)[y_col].sum().reset_index()
    totals["label"] = totals[y_col].apply(total_format_fn)

    fig.add_trace(
        go.Scatter(
            x=totals[x_col],
            y=totals[y_col],
            mode="text",
            text=totals["label"],
            textposition="top center",
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        barmode="stack",
        xaxis_type="category",
        height=500,
        hovermode="x unified",
    )
    return fig