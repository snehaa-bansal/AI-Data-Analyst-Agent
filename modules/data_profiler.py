import pandas as pd


def get_dataset_summary(df):
    """Return important dataset-level information."""

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    return {
        "rows": total_rows,
        "columns": total_columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
    }


def get_column_information(df):
    """Return data type, missing-value and unique-value information."""

    column_information = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean().mul(100).round(2).values
        ),
        "Unique Values": df.nunique(dropna=True).values,
    })

    return column_information


def get_numeric_summary(df):
    """Return descriptive statistics for numerical columns."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().T.round(2)


def get_categorical_summary(df):
    """Return descriptive information for categorical columns."""

    categorical_df = df.select_dtypes(
        include=["object", "category", "bool"]
    )

    if categorical_df.empty:
        return pd.DataFrame()

    summary_rows = []

    for column in categorical_df.columns:
        non_null_values = categorical_df[column].dropna()

        if non_null_values.empty:
            most_common = "No values"
            frequency = 0
        else:
            most_common = str(non_null_values.mode().iloc[0])
            frequency = int(
                (non_null_values == non_null_values.mode().iloc[0]).sum()
            )

        summary_rows.append({
            "Column": column,
            "Non-Null Values": int(non_null_values.shape[0]),
            "Unique Values": int(non_null_values.nunique()),
            "Most Common Value": most_common,
            "Frequency": frequency,
        })

    return pd.DataFrame(summary_rows)