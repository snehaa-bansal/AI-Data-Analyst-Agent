import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_column_types(df):
    """Return numerical and categorical column names."""

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns.tolist()

    return numerical_columns, categorical_columns


def create_histogram(df, column):
    return px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}",
        template="plotly_white",
    )


def create_box_plot(df, column):
    return px.box(
        df,
        y=column,
        title=f"Box Plot of {column}",
        template="plotly_white",
        points="outliers",
    )


def create_scatter_plot(df, x_column, y_column):
    return px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} vs {x_column}",
        template="plotly_white",
        opacity=0.7,
    )


def create_line_chart(df, x_column, y_column):
    chart_df = df[[x_column, y_column]].dropna()

    return px.line(
        chart_df,
        x=x_column,
        y=y_column,
        title=f"{y_column} Across {x_column}",
        template="plotly_white",
    )


def create_bar_chart(df, column):
    value_counts = (
        df[column]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .head(20)
        .reset_index()
    )

    value_counts.columns = [column, "Count"]

    return px.bar(
        value_counts,
        x=column,
        y="Count",
        title=f"Top Categories in {column}",
        template="plotly_white",
        color="Count",
        color_continuous_scale="Blues",
    )


def create_correlation_heatmap(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    correlation = numeric_df.corr()

    figure = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar={"title": "Correlation"},
        )
    )

    figure.update_layout(
        title="Correlation Heatmap",
        template="plotly_white",
        height=650,
    )

    return figure