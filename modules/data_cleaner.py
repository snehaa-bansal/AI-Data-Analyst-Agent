import numpy as np
import pandas as pd


def clean_dataset(
    df,
    convert_blanks=True,
    remove_duplicates=True,
    remove_empty=True,
    numeric_method="Median",
    categorical_method="Mode",
):
    """
    Create and return a cleaned copy of the dataset.
    """

    cleaned_df = df.copy()
    cleaning_log = []

    # Convert blank strings into missing values
    if convert_blanks:
        text_columns = cleaned_df.select_dtypes(
            include=["object", "string"]
        ).columns

        blank_count = 0

        for column in text_columns:
            current_blanks = int(
                cleaned_df[column]
                .fillna("")
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

            blank_count += current_blanks

            cleaned_df[column] = cleaned_df[column].replace(
                r"^\s*$",
                np.nan,
                regex=True,
            )

        cleaning_log.append(
            f"Converted {blank_count} blank text values "
            "into missing values."
        )

    # Remove duplicate rows
    if remove_duplicates:
        duplicate_count = int(cleaned_df.duplicated().sum())
        cleaned_df = cleaned_df.drop_duplicates()

        cleaning_log.append(
            f"Removed {duplicate_count} duplicate rows."
        )

    # Remove completely empty rows and columns
    if remove_empty:
        original_rows = len(cleaned_df)
        original_columns = cleaned_df.shape[1]

        cleaned_df = cleaned_df.dropna(
            axis=0,
            how="all",
        )

        cleaned_df = cleaned_df.dropna(
            axis=1,
            how="all",
        )

        removed_rows = original_rows - len(cleaned_df)
        removed_columns = (
            original_columns - cleaned_df.shape[1]
        )

        cleaning_log.append(
            f"Removed {removed_rows} completely empty rows "
            f"and {removed_columns} completely empty columns."
        )

    # Fill numerical missing values
    numeric_columns = cleaned_df.select_dtypes(
        include="number"
    ).columns

    numerical_values_filled = 0

    for column in numeric_columns:
        missing_count = int(
            cleaned_df[column].isnull().sum()
        )

        if missing_count == 0:
            continue

        if numeric_method == "Median":
            fill_value = cleaned_df[column].median()

        elif numeric_method == "Mean":
            fill_value = cleaned_df[column].mean()

        elif numeric_method == "Zero":
            fill_value = 0

        else:
            continue

        if pd.notna(fill_value):
            cleaned_df[column] = (
                cleaned_df[column].fillna(fill_value)
            )

            numerical_values_filled += missing_count

    cleaning_log.append(
        f"Filled {numerical_values_filled} missing numerical "
        f"values using: {numeric_method}."
    )

    # Fill categorical missing values
    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns

    categorical_values_filled = 0

    for column in categorical_columns:
        missing_count = int(
            cleaned_df[column].isnull().sum()
        )

        if missing_count == 0:
            continue

        if categorical_method == "Mode":
            mode_values = cleaned_df[column].mode()

            fill_value = (
                mode_values.iloc[0]
                if not mode_values.empty
                else "Unknown"
            )

        elif categorical_method == "Unknown":
            fill_value = "Unknown"

        else:
            continue

        cleaned_df[column] = (
            cleaned_df[column].fillna(fill_value)
        )

        categorical_values_filled += missing_count

    cleaning_log.append(
        f"Filled {categorical_values_filled} missing "
        f"categorical values using: {categorical_method}."
    )

    cleaned_df = cleaned_df.reset_index(drop=True)

    return cleaned_df, cleaning_log