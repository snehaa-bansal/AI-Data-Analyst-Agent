import pandas as pd


def detect_data_quality_issues(df):
    """
    Detect common data-quality problems.
    """

    issues = []

    # Missing values
    for column in df.columns:
        missing_count = int(df[column].isnull().sum())

        if missing_count > 0:
            missing_percentage = round(
                (missing_count / len(df)) * 100,
                2
            )

            issues.append({
                "Issue Type": "Missing Values",
                "Column": column,
                "Count": missing_count,
                "Percentage": missing_percentage,
                "Recommendation": (
                    "Fill or remove missing values"
                ),
            })

    # Exact duplicate rows
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        issues.append({
            "Issue Type": "Duplicate Rows",
            "Column": "Entire Dataset",
            "Count": duplicate_count,
            "Percentage": round(
                (duplicate_count / len(df)) * 100,
                2
            ),
            "Recommendation": "Remove duplicate rows",
        })

    # Constant columns
    for column in df.columns:
        if df[column].nunique(dropna=False) <= 1:
            issues.append({
                "Issue Type": "Constant Column",
                "Column": column,
                "Count": len(df),
                "Percentage": 100.0,
                "Recommendation": (
                    "Consider removing this column"
                ),
            })

    # Blank text values
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        blank_count = int(
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if blank_count > 0:
            issues.append({
                "Issue Type": "Blank Text",
                "Column": column,
                "Count": blank_count,
                "Percentage": round(
                    (blank_count / len(df)) * 100,
                    2
                ),
                "Recommendation": (
                    "Convert blank text into missing values"
                ),
            })

    # IQR-based numerical outliers
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        values = df[column].dropna()

        if values.nunique() < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outlier_count = int(
            (
                (values < lower_limit) |
                (values > upper_limit)
            ).sum()
        )

        if outlier_count > 0:
            issues.append({
                "Issue Type": "Possible Outliers",
                "Column": column,
                "Count": outlier_count,
                "Percentage": round(
                    (outlier_count / len(df)) * 100,
                    2
                ),
                "Recommendation": (
                    "Review before removing or capping"
                ),
            })

    return pd.DataFrame(issues)