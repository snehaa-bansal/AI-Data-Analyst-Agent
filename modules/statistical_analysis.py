import pandas as pd


def calculate_numeric_statistics(df):
    """
    Calculate statistical measures for numerical columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    statistics = pd.DataFrame({
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Standard Deviation": numeric_df.std(),
        "Variance": numeric_df.var(),
        "Minimum": numeric_df.min(),
        "Maximum": numeric_df.max(),
        "Range": numeric_df.max() - numeric_df.min(),
        "Skewness": numeric_df.skew(),
        "Kurtosis": numeric_df.kurtosis(),
    })

    statistics.index.name = "Column"

    return statistics.reset_index().round(4)


def interpret_skewness(skewness):
    """Convert a skewness value into an interpretation."""

    if pd.isna(skewness):
        return "Cannot Determine"

    if skewness > 1:
        return "Highly Right-Skewed"

    if skewness > 0.5:
        return "Moderately Right-Skewed"

    if skewness < -1:
        return "Highly Left-Skewed"

    if skewness < -0.5:
        return "Moderately Left-Skewed"

    return "Approximately Symmetrical"


def get_distribution_analysis(df):
    """
    Analyse the distribution of numerical columns.
    """

    numeric_df = df.select_dtypes(include="number")

    results = []

    for column in numeric_df.columns:
        skewness = numeric_df[column].skew()

        results.append({
            "Column": column,
            "Skewness": round(skewness, 4),
            "Distribution": interpret_skewness(skewness),
        })

    return pd.DataFrame(results)


def find_correlations(df, threshold=0.5):
    """
    Find numerical column pairs with correlation equal to or
    greater than the selected absolute threshold.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return pd.DataFrame()

    correlation_matrix = numeric_df.corr()

    relationships = []

    columns = correlation_matrix.columns

    for first_index in range(len(columns)):
        for second_index in range(first_index + 1, len(columns)):
            first_column = columns[first_index]
            second_column = columns[second_index]

            correlation = correlation_matrix.loc[
                first_column,
                second_column,
            ]

            if pd.isna(correlation):
                continue

            if abs(correlation) >= threshold:
                absolute_correlation = abs(correlation)

                if absolute_correlation >= 0.8:
                    strength = "Very Strong"
                elif absolute_correlation >= 0.6:
                    strength = "Strong"
                else:
                    strength = "Moderate"

                direction = (
                    "Positive"
                    if correlation > 0
                    else "Negative"
                )

                relationships.append({
                    "First Column": first_column,
                    "Second Column": second_column,
                    "Correlation": round(correlation, 4),
                    "Strength": strength,
                    "Direction": direction,
                })

    if not relationships:
        return pd.DataFrame()

    correlation_results = pd.DataFrame(relationships)

    correlation_results["Absolute Correlation"] = (
        correlation_results["Correlation"].abs()
    )

    correlation_results = correlation_results.sort_values(
        by="Absolute Correlation",
        ascending=False,
    ).drop(columns=["Absolute Correlation"])

    return correlation_results.reset_index(drop=True)